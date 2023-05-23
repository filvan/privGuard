from src.examples.program.traccar.networkMessage import NetworkMessage
from src.examples.program.traccar.helper.networkUtil import NetworkUtil


class StandardLoggingHandler():

    _LOGGER = "LoggerFactory.getLogger(StandardLoggingHandler.class)"


    def __init__(self, protocol):

        self._protocol = None

        self._protocol = protocol

    def channelRead(self, ctx, msg):
        self.log(ctx, False, msg)
        super().channelRead(ctx, msg)

    def write(self, ctx, msg, promise):
        self.log(ctx, True, msg)
        super().write(ctx, msg, promise)

    def log(self, ctx, downstream, o):
        if isinstance(o, NetworkMessage):
            networkMessage = o
            if isinstance(networkMessage.getMessage(), bytes):
                self.log(ctx, downstream, networkMessage.getRemoteAddress(), networkMessage.getMessage())
        elif isinstance(o, bytes):
            self.log(ctx, downstream, ctx.channel().remoteAddress(), o)

    def log(self, ctx, downstream, remoteAddress, buf):
        message = ""

        message+= ("[")+ (NetworkUtil.session(ctx.channel()))+ (": ")
        message+= (self._protocol)
        if downstream:
            message+= (" > ")
        else:
            message+= (" < ")

        if isinstance(remoteAddress, "InetSocketAddress"):
            message+= ((remoteAddress).getHostString())
        else:
            message+= ("unknown")
        message+= ("] ")

        message+= ("ByteBufUtil".hexDump(buf))

        StandardLoggingHandler._LOGGER.info(str(message))
