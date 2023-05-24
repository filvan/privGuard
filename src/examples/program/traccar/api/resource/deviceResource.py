from kafka.protocol.api import Response

from src.examples.program.traccar.api.baseObjectResource import BaseObjectResource
from src.examples.program.traccar.broadcast.broadcastService import BroadcastService
from src.examples.program.traccar.database.mediaManager import MediaManager
from src.examples.program.traccar.helper.logAction import LogAction
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.deviceAccumulator import DeviceAccumulators
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.session.connectionManager import ConnectionManager
from src.examples.program.traccar.session.cache.cacheManager import CacheManager
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class DeviceResource(BaseObjectResource):

    def __init__(self):

        self._cacheManager = None
        self._connectionManager = None
        self._broadcastService = None
        self._mediaManager = None

        super().__init__(Device.__class__)

    def get(self, all, userId, uniqueIds, deviceIds):

        if uniqueIds or deviceIds:

            result = list()
            for uniqueId in uniqueIds:
                result.extend(self.storage.getObjects(Device.__class__, Request(Columns.All(), Condition.And(Condition.Equals("uniqueId", uniqueId), Condition.Permission(User.__class__, self.getUserId(), Device.__class__)))))
            for deviceId in deviceIds:
                result.extend(self.storage.getObjects(Device.__class__, Request(Columns.All(), Condition.And(Condition.Equals("id", deviceId), Condition.Permission(User.__class__, self.getUserId(), Device.__class__)))))
            return result

        else:

            conditions = list()

            if all:
                if self.permissionsService.notAdmin(self.getUserId()):
                    conditions.append(Condition.Permission(User.__class__, self.getUserId(), self.baseClass))
            else:
                if userId == 0:
                    conditions.append(Condition.Permission(User.__class__, self.getUserId(), self.baseClass))
                else:
                    self.permissionsService.checkUser(self.getUserId(), userId)
                    conditions.append((Condition.Permission(User.__class__, userId, self.baseClass)).excludeGroups())

            return self.storage.getObjects(self.baseClass, Request(Columns.All(), Condition.merge(conditions)))


    def updateAccumulators(self, entity):
        if self.permissionsService.notAdmin(self.getUserId()):
            self.permissionsService.checkManager(self.getUserId())
            self.permissionsService.checkPermission(Device.__class__, self.getUserId(), entity.getDeviceId())

        position = self.storage.getObject(Position.__class__, Request(Columns.All(), Condition.LatestPositions(entity.getDeviceId())))
        if position is not None:
            if entity.getTotalDistance() is not None:
                position.getAttributes().put(Position.KEY_TOTAL_DISTANCE, entity.getTotalDistance())
            if entity.getHours() is not None:
                position.getAttributes().put(Position.KEY_HOURS, entity.getHours())
            position.setId(self.storage.addObject(position, Request(Columns.Exclude("id"))))

            device = Device()
            device.setId(position.getDeviceId())
            device.setPositionId(position.getId())
            self.storage.updateObject(device, Request(Columns.Include("positionId"), Condition.Equals("id", device.getId())))

            try:
                self._cacheManager.addDevice(position.getDeviceId())
                self._cacheManager.updatePosition(position)
                self._connectionManager.updatePosition(True, position)
            finally:
                self._cacheManager.removeDevice(position.getDeviceId())
        else:
            raise Exception

        LogAction.resetDeviceAccumulators(self.getUserId(), entity.getDeviceId())
        return Response.noContent().build()

    def uploadImage(self, deviceId, file, type):

        device = self.storage.getObject(Device.__class__, Request(Columns.All(), Condition.And(Condition.Equals("id", deviceId), Condition.Permission(User.__class__, self.getUserId(), Device.__class__))))
        if device is not None:
            name = "device"
            extension = type[len("image/"):]
            with "FileInputStream(file)" as input, self.mediaManager.createFileStream(device.getUniqueId(), name, extension) as output:
                input.transferTo(output)
            return Response.ok(name + "." + extension).build()
        return Response.status(Response.Status.NOT_FOUND).build()
