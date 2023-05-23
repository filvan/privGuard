from src.examples.program.traccar.forward.networkForwarder import NetworkForwarder

class NetworkForwarderHandler():



    def __init__(self, port):

        self._port = 0
        self._networkForwarder = None

        self._port = port

    def setNetworkForwarder(self, networkForwarder):
        self._networkForwarder = networkForwarder

    def channelRead(self, ctx, msg):
        datagram = isinstance(ctx.channel(), "DatagramChannel")
        remoteAddress = None
        buffer = None
        if datagram:
            message = msg
            remoteAddress = message.recipient()
            buffer = message.content()
        else:
            remoteAddress = ctx.channel().remoteAddress()
            buffer = msg

        data = [0 for _ in range(buffer.readableBytes())]
        buffer.getBytes(buffer.readerIndex(), data)
        self._networkForwarder.forward(remoteAddress, self._port, datagram, data)
        super().channelRead(ctx, msg)

    def channelInactive(self, ctx):
        if not(isinstance(ctx.channel(), "DatagramChannel")):
            self._networkForwarder.disconnect(ctx.channel().remoteAddress())
        super().channelInactive(ctx)
