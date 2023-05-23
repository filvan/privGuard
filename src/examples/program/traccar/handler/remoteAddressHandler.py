from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.model.position import Position

class RemoteAddressHandler():


    def __init__(self, config):

        self._enabled = False

        self._enabled = config.getBoolean(Keys.PROCESSING_REMOTE_ADDRESS_ENABLE)

    def channelRead(self, ctx, msg):

        if self._enabled:
            remoteAddress = ctx.channel().remoteAddress()
            hostAddress = remoteAddress.getAddress().getHostAddress() if remoteAddress is not None else None

            if isinstance(msg, Position):
                position = msg
                position.set(Position.KEY_IP, hostAddress)

        ctx.fireChannelRead(msg)
