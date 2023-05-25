from src.examples.program.traccar.baseFrameDecoder import BaseFrameDecoder

class AplicomFrameDecoder(BaseFrameDecoder):

    def decode(self, ctx, channel, buf):


        while buf.isReadable() and (buf.getByte(buf.readerIndex())).isdigit():
            buf.readByte()


        if buf.readableBytes() < 11:
            return None


        version = buf.getUnsignedByte(buf.readerIndex() + 1)
        offset = 1 + 1 + 3
        if (version & 0x80) != 0:
            offset += 4


        length = buf.getUnsignedShort(buf.readerIndex() + offset)
        offset += 2
        if (version & 0x40) != 0:
            offset += 3
        length += offset


        if buf.readableBytes() >= length:
            return buf.readRetainedSlice(length)

        return None
