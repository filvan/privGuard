from kafka.protocol.api import Response

from src.examples.program.traccar.api.baseObjectResource import BaseObjectResource
from src.examples.program.traccar.broadcast.broadcastService import BroadcastService
from src.examples.program.traccar.config import config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.database.mediaManager import MediaManager
from src.examples.program.traccar.helper.logAction import LogAction
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.deviceAccumulator import DeviceAccumulators
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.session.connectionManager import ConnectionManager
from src.examples.program.traccar.session.cache.cacheManager import CacheManager
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition, And, Equals, Permission, LatestPositions
from src.examples.program.traccar.storage.query.request import Request


class DeviceResource(BaseObjectResource):

    def __init__(self):

        self.DEFAULT_BUFFER_SIZE = 8192
        self.IMAGE_SIZE_LIMIT = 500000

        self.config = None
        self.cache_manager = None
        self.connection_manager = None
        self.broadcast_service = None
        self.media_manager = None
        self.token_manager = None
        super().__init__(Device.__class__)

    def get(self, all, userId, uniqueIds, deviceIds):

        if len(uniqueIds) > 0 or len(deviceIds) > 0:

            result = list()
            for uniqueId in uniqueIds:
                result.extend(self.storage.getObjects(Device.__class__, Request(Columns.All(), And(
                    Equals("uniqueId", uniqueId),
                    Permission(User.__class__, self.get_user_id(), Device.__class__)))))
            for deviceId in deviceIds:
                result.extend(self.storage.getObjects(Device.__class__, Request(Columns.All(), And(
                    Equals("id", deviceId),
                    Permission(User.__class__, self.get_user_id(), Device.__class__)))))
            return result

        else:

            conditions = list()

            if all:
                if self.permissions_service.notAdmin(self.get_user_id()):
                    conditions.append(Permission(User.__class__, self.get_user_id(), self.base_class))
            else:
                if userId == 0:
                    conditions.append(Permission(User.__class__, self.get_user_id(), self.base_class))
                else:
                    self.permissions_service.checkUser(self.get_user_id(), userId)
                    conditions.append((Permission(User.__class__, userId, self.base_class)).do_exclude_groups())

            return self.storage.getObjects(self.base_class, Request(Columns.All(), Condition.merge(conditions)))

    def update_accumulators(self, entity):
        self.permissions_service.checkPermission(Device.__class__, self.get_user_id(), entity.getDeviceId())
        self.permissions_service.checkEdit(getUserId(), Device.__class__, false, false)

        position = self.storage.getObject(Position.__class__,
                                          Request(Columns.All(), LatestPositions(entity.getDeviceId())))
        if position is not None:
            if entity.getTotalDistance() is not None:
                position.getAttributes().put(Position.KEY_TOTAL_DISTANCE, entity.getTotalDistance())
            if entity.getHours() is not None:
                position.getAttributes().put(Position.KEY_HOURS, entity.getHours())
            position.setId(self.storage.addObject(position, Request(Columns.Exclude("id"))))

            device = Device()
            device.setId(position.getDeviceId())
            device.setPositionId(position.getId())
            self.storage.updateObject(device,
                                      Request(Columns.Include("positionId"), Equals("id", device.getId())))
            key = []
            try:
                self.cache_manager.addDevice(position.getDeviceId(), key)
                self.cache_manager.updatePosition(position)
                self.connection_manager.updatePosition(True, position)
            finally:
                self.cache_manager.removeDevice(position.getDeviceId(), key)
        else:
            raise Exception

        LogAction.resetDeviceAccumulators(self.get_user_id(), entity.getDeviceId())
        return Response.noContent().build()

    def image_extension(self, type):
        if type == "image/jpeg":
            return "jpg"
        elif type == "image/png":
            return "png"
        elif type == "image/gif":
            return "gif"
        elif type == "image/webp":
            return "webp"
        elif type == "image/svg":
            return "svg"
        else:
            raise Exception

    def upload_image(self, deviceId, file, type):

        device = self.storage.getObject(Device.__class__, Request(Columns.All(),
                                                                  And(Equals("id", deviceId),
                                                                      Permission(User.__class__,
                                                                                 self.get_user_id(),
                                                                                 Device.__class__))))
        if device is not None:
            name = "device"
            extension = self.image_extension(type)
            with open(file, 'rb') as input_file, self.media_manager.create_file_stream(device.get_unique_id(), name,
                                                                                       extension) as output_file:
                transferred = 0
                buffer = bytearray(self.DEFAULT_BUFFER_SIZE)
                while True:
                    read = input_file.readinto(buffer)
                    if read == 0:
                        break
                    output_file.write(buffer[:read])
                    transferred += read
                    if transferred > self.IMAGE_SIZE_LIMIT:
                        raise ValueError("Image size limit exceeded")

            return Response.ok(name + "." + extension).build()
        return Response.ok(Response.Status.NOT_FOUND).build()

    def share_device(self, device_id, expiration):
        user = self.permissions_service.get_user(self.get_user_id())
        if self.permissions_service.get_server().get_boolean(Keys.DEVICE_SHARE_DISABLE.get_key()):
            raise Exception("Sharing is disabled")
        if user.get_temporary():
            raise Exception("Temporary user")
        if user.get_expiration_time() and user.get_expiration_time().before(expiration):
            expiration = user.get_expiration_time()

        device: Device = Storage.getObject(Device, Request(
            Columns.All(),
            And(
                Equals("id", device_id),
                Permission(User.__class__, user.get_id(), Device.__class__))))

        share_email = f"{user.get_email()}:{device.getUniqueId()}"
        share = Storage.getObject(User, Request(
            Columns.All(), Equals("email", share_email)
        ))

        if share is None:
            share = User()
            share.setName(device.getName())
            share.setEmail(share_email)
            share.setExpirationTime(expiration)
            share.setTemporary(True)
            share.setReadonly(True)
            share.setLimitCommands(
                user.get_limit_commands() or not config.get_boolean(Keys.WEB_SHARE_DEVICE_COMMANDS))
            share.setDisableReports(
                user.get_disable_reports() or not config.get_boolean(Keys.WEB_SHARE_DEVICE_REPORTS))

            share.setId(Storage.addObject(share, Request(Columns.Exclude("id"))))

            Storage.addPermission(Permission(User, share.get_id(), Device, device_id))

        return self.token_manager.generate_token(share.get_id(), expiration)
