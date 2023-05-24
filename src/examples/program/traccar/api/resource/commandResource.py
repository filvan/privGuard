import collections

from kafka.protocol.api import Response

from src.examples.program.traccar.baseProtocol import BaseProtocol
from src.examples.program.traccar.serverManager import ServerManager
from src.examples.program.traccar.api.extendedObjectResource import ExtendedObjectResource
from src.examples.program.traccar.database.commandsManager import CommandsManager
from src.examples.program.traccar.helper.model.deviceUtil import DeviceUtil
from src.examples.program.traccar.model.command import Command
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.group import Group
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.queuedCommand import QueuedCommand
from src.examples.program.traccar.model.typed import Typed
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.model.userRestriction import UserRestrictions
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class CommandResource(ExtendedObjectResource):

    _LOGGER = "LoggerFactory.getLogger(CommandResource.__class__)"



    def __init__(self):
        #instance fields found by Java to Python Converter:
        self._commandsManager = None
        self._serverManager = None

        super().__init__(Command.__class__)

    def _getDeviceProtocol(self, deviceId):
        position = self.storage.getObject(Position.__class__, Request(Columns.All(), Condition.LatestPositions(deviceId)))
        if position is not None:
            return self._serverManager.getProtocol(position.getProtocol())
        else:
            return None

    def get(self, deviceId):
        self.permissionsService.checkPermission(Device.__class__, self.getUserId(), deviceId)
        protocol = self._getDeviceProtocol(deviceId)

        commands = self.storage.getObjects(self.baseClass, Request(Columns.All(), Condition.merge(list.append(Condition.Permission(User.__class__, self.getUserId(), self.baseClass), Condition.Permission(Device.__class__, deviceId, self.baseClass)))))

        #JAVA TO PYTHON CONVERTER TASK: Only expression lambdas are converted by Java to Python Converter:
        #        return commands.stream().filter(command ->
        #        {
        #            String type = command.getType()
        #            if (protocol != null)
        #            {
        #                return command.getTextChannel() && protocol.getSupportedTextCommands().contains(type) || !command.getTextChannel() && protocol.getSupportedDataCommands().contains(type)
        #            }
        #            else
        #            {
        #                return type.equals(Command.TYPE_CUSTOM)
        #            }
        #        }
        #        ).collect(Collectors.toList())

    def send(self, entity, groupId):
        if entity.getId() > 0:
            self.permissionsService.checkPermission(self.baseClass, self.getUserId(), entity.getId())
            deviceId = entity.getDeviceId()
            entity = self.storage.getObject(self.baseClass, Request(Columns.All(), Condition.Equals("id", entity.getId())))
            entity.setDeviceId(deviceId)
        else:
            self.permissionsService.checkRestriction(self.getUserId(), UserRestrictions.getLimitCommands())
        result = True
        if groupId > 0:
            self.permissionsService.checkPermission(Group.__class__, self.getUserId(), groupId)
            devices = DeviceUtil.getAccessibleDevices(self.storage, self.getUserId(), list(), list(groupId))
            for device in devices:
                command = QueuedCommand.fromCommand(entity).toCommand()
                command.setDeviceId(device.getId())
                result = self._commandsManager.sendCommand(command) and result
        else:
            self.checkPermission(Device.__class__, self.getUserId(), entity.getDeviceId())
            result = self._commandsManager.sendCommand(entity)
        return Response.ok(entity).build() if result else Response.accepted(entity).build()

    def get(self, deviceId, textChannel):
        if deviceId != 0:
            self.checkPermission(Device.__class__, self.getUserId(), deviceId)
            protocol = self._getDeviceProtocol(deviceId)
            if protocol is not None:
                if textChannel:
                    return protocol.getSupportedTextCommands().stream().map(Typed()).collect(collections.toList())
                else:
                    return protocol.getSupportedDataCommands().stream().map(Typed()).collect(collections.toList())
            else:
                return collections.singletonList(Typed(Command.TYPE_CUSTOM))
        else:
            result = []
            fields = Command.__class__.getDeclaredFields()
            for field in fields:
                if "Modifier.isStatic(field.getModifiers())" and field.getName().startsWith("TYPE_"):
                    try:
                        result.append(Typed(str(field.get(None))))
                    except Exception as error:
                        CommandResource._LOGGER.warn("Get command types error", error)
            return result
