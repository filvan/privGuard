from src.examples.program.traccar.networkMessage import NetworkMessage

class AlematicsFrameDecoder():

    _MESSAGE_MINIMUM_LENGTH = 2

    def __init__(self, maxFrameLength):
        super().__init__(maxFrameLength)

    def decode(self, ctx, buf):

        if buf.readableBytes() < AlematicsFrameDecoder._MESSAGE_MINIMUM_LENGTH:
            return None

        if buf.getUnsignedShort(buf.readerIndex()) == 0xFAF8:
            heartbeat = buf.readRetainedSlice(12)
            if ctx is not None and ctx.channel() is not None:
                ctx.channel().writeAndFlush(NetworkMessage(heartbeat, ctx.channel().remoteAddress()))

        return super().decode(ctx, buf)
