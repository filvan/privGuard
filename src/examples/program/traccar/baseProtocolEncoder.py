from src.examples.program.traccar.helper.networkUtil import NetworkUtil
from src.examples.program.traccar.helper.model.attributeUtil import AttributeUtil
from src.examples.program.traccar.model.command import Command
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.networkMessage import NetworkMessage
from src.examples.program.traccar.session.cache.cacheManager import CacheManager

class BaseProtocolEncoder():

    _LOGGER = "LoggerFactory.getLogger(BaseProtocolEncoder.__class__)"

    _PROTOCOL_UNKNOWN = "unknown"



    def __init__(self, protocol):

        self._protocol = None
        self._cacheManager = None

        self._protocol = protocol

    def getCacheManager(self):
        return self._cacheManager

    def setCacheManager(self, cacheManager):
        self._cacheManager = cacheManager

    def getProtocolName(self):
        return self._protocol.getName() if self._protocol is not None else BaseProtocolEncoder._PROTOCOL_UNKNOWN

    def getUniqueId(self, deviceId):
        return self._cacheManager.getObject(Device.__class__, deviceId).getUniqueId()

    def initDevicePassword(self, command, defaultPassword):
        if not command.hasAttribute(Command.KEY_DEVICE_PASSWORD):
            password = AttributeUtil.getDevicePassword(self._cacheManager, command.getDeviceId(), self.getProtocolName(), defaultPassword)
            command.set(Command.KEY_DEVICE_PASSWORD, password)

    def write(self, ctx, msg, promise):

        if isinstance(msg, NetworkMessage):
            networkMessage = msg
            if isinstance(networkMessage.getMessage(), Command):

                command = networkMessage.getMessage()
                encodedCommand = self.encodeCommand(ctx.channel(), command)

                s = ""
                s += ("[") + (NetworkUtil.session(ctx.channel())) + ("] ")
                s += ("id: ") + (self.getUniqueId(command.getDeviceId())) + (", ")
                s += ("command type: ") + (command.getType()) + (" ")
                if encodedCommand is not None:
                    s += ("sent")
                else:
                    s += ("not sent")
                BaseProtocolEncoder._LOGGER.info(str(s))

                ctx.write(NetworkMessage(encodedCommand, networkMessage.getRemoteAddress()), promise)

                return
        super().write(ctx, msg, promise)

    def encodeCommand(self, channel, command):
        return self.encodeCommand(command)

    def encodeCommand(self, command):
        return None
