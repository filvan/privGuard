import http

from src.examples.program.traccar.model.command import Command
from src.examples.program.traccar.protocol import Protocol
from src.examples.program.traccar.basePipelineFactory import BasePipelineFactory
from src.examples.program.traccar.protocol import Protocol
from src.examples.program.traccar.model.command import Command

class DeviceSession:


    def __init__(self, deviceId, uniqueId, protocol, channel, remoteAddress):

        self._deviceId = 0
        self._uniqueId = None
        self._protocol = None
        self._channel = None
        self._remoteAddress = None
        self._locals = {}

        self._deviceId = deviceId
        self._uniqueId = uniqueId
        self._protocol = protocol
        self._channel = channel
        self._remoteAddress = remoteAddress

    def getDeviceId(self):
        return self._deviceId

    def getUniqueId(self):
        return self._uniqueId

    def getChannel(self):
        return self._channel

    def getRemoteAddress(self):
        return self._remoteAddress

    def supportsLiveCommands(self):
        return BasePipelineFactory.getHandler(self._channel.pipeline(), http.__class__) is None

    def sendCommand(self, command):
        self._protocol.sendDataCommand(self._channel, self._remoteAddress, command)

    KEY_TIMEZONE = "timezone"


    def contains(self, key):
        return key in self._locals.keys()

    def set(self, key, value):
        if value is not None:
            self._locals[key] = value
        else:
            self._locals.pop(key)

    def get(self, key):
        return self._locals[key]
