from src.examples.program.traccar.networkMessage import NetworkMessage

class NetworkMessageHandler():

    def channelRead(self, ctx, msg):
        if isinstance(ctx.channel(), "DatagramChannel"):
            packet = msg
            ctx.fireChannelRead(NetworkMessage(packet.content(), packet.sender()))
        elif isinstance(msg, bytes):
            buffer = msg
            ctx.fireChannelRead(NetworkMessage(buffer, ctx.channel().remoteAddress()))

    def write(self, ctx, msg, promise):
        if isinstance(msg, NetworkMessage):
            message = msg
            if isinstance(ctx.channel(), "DatagramChannel"):
                recipient = message.getRemoteAddress()
                sender = ctx.channel().localAddress()
                ctx.write("datagramPacket(message.getMessage(), recipient, sender)", promise)
            else:
                ctx.write(message.getMessage(), promise)
        else:
            ctx.write(msg, promise)
