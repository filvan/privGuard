import collections

from src.examples.program.traccar.baseProtocol import BaseProtocol
from src.examples.program.traccar.serverManager import ServerManager
from src.examples.program.traccar.broadcast.broadcastInterface import BroadcastInterface
from src.examples.program.traccar.broadcast.broadcastService import BroadcastService
from src.examples.program.traccar.model.command import Command
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.queuedCommand import QueuedCommand
from src.examples.program.traccar.session.connectionManager import ConnectionManager
from src.examples.program.traccar.session.deviceSession import DeviceSession
from src.examples.program.traccar.sms.smsManager import SmsManager
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.order import Order
from src.examples.program.traccar.storage.query.request import Request

class CommandsManager(BroadcastInterface):


    def __init__(self, storage, serverManager, smsManager, connectionManager, broadcastService):

        self._storage = None
        self._serverManager = None
        self._smsManager = None
        self._connectionManager = None
        self._broadcastService = None

        self._storage = storage
        self._serverManager = serverManager
        self._smsManager = smsManager
        self._connectionManager = connectionManager
        self._broadcastService = broadcastService
        broadcastService.registerListener(self)

    def sendCommand(self, command):
        deviceId = command.getDeviceId()
        if command.getTextChannel():
            if self._smsManager is None:
                raise Exception("SMS not configured")
            device = self._storage.getObject(Device.__class__, Request(Columns.Include("positionId", "phone"), Condition.Equals("id", deviceId)))
            position = self._storage.getObject(Position.__class__, Request(Columns.All(), Condition.Equals("id", device.getPositionId())))
            if position is not None:
                protocol = self._serverManager.getProtocol(position.getProtocol())
                protocol.sendTextCommand(device.getPhone(), command)
            elif command.getType() is Command.TYPE_CUSTOM:
                self._smsManager.sendMessage(device.getPhone(), command.getString(Command.KEY_DATA), True)
            else:
                raise Exception("Command " + command.getType() + " is not supported")
        else:
            deviceSession = self._connectionManager.getDeviceSession(deviceId)
            if deviceSession is not None and deviceSession.supportsLiveCommands():
                deviceSession.sendCommand(command)
            else:
                self._storage.addObject(QueuedCommand.fromCommand(command), Request(Columns.Exclude("id")))
                self._broadcastService.updateCommand(True, deviceId)
                return False
        return True

    def readQueuedCommands(self, deviceId):
        return self.readQueuedCommands(deviceId, int.MAX_VALUE)

    def readQueuedCommands(self, deviceId, count):
        try:
            commands = self._storage.getObjects(QueuedCommand.__class__, Request(Columns.All(), Condition.Equals("deviceId", deviceId), Order("id", False, count)))
            for command in commands:
                self._storage.removeObject(QueuedCommand.__class__, Request(Condition.Equals("id", command.getId())))
            return commands.stream().map(QueuedCommand.toCommand()).collect(collections.toList())
        except StorageException as e:
            raise Exception(e)

    def updateCommand(self, local, deviceId):
        if not local:
            deviceSession = self._connectionManager.getDeviceSession(deviceId)
            if deviceSession is not None and deviceSession.supportsLiveCommands():
                for command in self.readQueuedCommands(deviceId):
                    deviceSession.sendCommand(command)
