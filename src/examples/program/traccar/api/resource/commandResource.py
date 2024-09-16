import collections
import inspect
import logging
from kafka.protocol.api import Response

from src.examples.program.traccar.baseProtocol import BaseProtocol
from src.examples.program.traccar.database import commandsManager
from src.examples.program.traccar.helper.logAction import LogAction
from src.examples.program.traccar.model import command
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
from src.examples.program.traccar.storage.query.condition import Condition, Permission, LatestPositions, Equals
from src.examples.program.traccar.storage.query.request import Request


class CommandResource(ExtendedObjectResource):
    LOGGER = "LoggerFactory.getLogger(CommandResource.__class__)"

    def __init__(self):
        self.commands_manager = None
        self.server_manager = None
        super().__init__(Command.__class__)

    def get_device_protocol(self, deviceId):
        position = self.storage.getObject(Position.__class__,
                                          Request(Columns.All(), LatestPositions(deviceId)))
        if position is not None:
            return self.server_manager.getProtocol(position.getProtocol())
        else:
            return None

    def get(self, deviceId):
        self.permissions_service.checkPermission(Device, self.get_user_id(), deviceId)
        protocol = self.get_device_protocol(deviceId)

        commands = self.storage.getObjects(self.base_class, Request(
            Columns.All(),
            Condition.merge(
                [Permission(User, self.get_user_id(), self.base_class),
                Permission(Device, deviceId, self.base_class)
             ])
        ))

        return [
            command for command in commands
            if (protocol is not None and (
                    (command.get_text_channel() and command.get_type() in protocol.get_supported_text_commands()) or
                    (not command.get_text_channel() and command.get_type() in protocol.get_supported_data_commands())
            )) or (protocol is None and command.get_type() == Command.TYPE_CUSTOM)
        ]

    def send(self, entity, groupId):
        if entity.getId() > 0:
            self.permissions_service.checkPermission(self.base_class, self.get_user_id(), entity.getId())
            deviceId = entity.getDeviceId()
            entity = self.storage.getObject(self.base_class,
                                            Request(Columns.All(), Equals("id", entity.getId())))
            entity.setDeviceId(deviceId)
        else:
            self.permissions_service.checkRestriction(self.get_user_id(), UserRestrictions.getLimitCommands())

        if groupId > 0:
            self.permissions_service.checkPermission(Group.__class__, self.get_user_id(), groupId)
            devices = DeviceUtil.getAccessibleDevices(self.storage, self.get_user_id(), list(), list(groupId))
            queuedCommands = []
            for device in devices:
                command = QueuedCommand.fromCommand(entity).toCommand()
                command.setDeviceId(device.getId())
                queuedCommand = CommandsManager.sendCommand(command)
                if queuedCommand is not None:
                    queuedCommands.append(queuedCommand)
            if len(queuedCommands) > 0:
                return Response.accepted(queuedCommands).build()
        else:
            self.permissions_service.checkPermission(Device, self.get_user_id(), entity.getDeviceId())
            queuedCommand = CommandsManager.sendCommand(entity)
            if queuedCommand is not None:
                return Response.accepted(queuedCommand).build()

        LogAction.command(self.get_user_id(), groupId, entity.getDeviceId(), entity.getType())
        return Response.ok(entity).build()

    def get(self, deviceId, textChannel):
        if deviceId != 0:
            self.permissions_service.checkPermission(Device, self.get_user_id(), deviceId)
            protocol = self.get_device_protocol(deviceId)
            if protocol is not None:
                if textChannel:
                    return [Typed(command) for command in protocol.get_supported_text_commands()]
                else:
                    return [Typed(command) for command in protocol.get_supported_data_commands()]
            else:
                return [Typed(Command.TYPE_CUSTOM)]
        else:
            result = []
            fields = inspect.getmembers(Command, lambda a: not (inspect.isroutine(a)))

            for name, value in fields:
                if name.startswith("TYPE_"):
                    try:
                        result.append(Typed(value))
                    except Exception as error:
                        logging.warning("Get command types error", error)
            return result
