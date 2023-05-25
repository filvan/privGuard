from src.examples.program.traccar.baseFrameDecoder import BaseFrameDecoder

class AdmFrameDecoder(BaseFrameDecoder):

    def decode(self, ctx, channel, buf):

        if buf.readableBytes() < 15 + 3:
            return None

        length = 0
        if (buf.getUnsignedByte(buf.readerIndex())).isdigit():
            length = 15 + buf.getUnsignedByte(buf.readerIndex() + 15 + 2)
        else:
            length = buf.getUnsignedByte(buf.readerIndex() + 2)

        if buf.readableBytes() >= length:
            return buf.readRetainedSlice(length)

        return None
