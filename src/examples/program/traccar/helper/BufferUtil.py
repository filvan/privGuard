
from .bitUtil import BitUtil
from .bitBuffer import BitBuffer
class BufferUtil:

    def __init__(self):
        pass

    @staticmethod
    def readSignedMagnitudeInt(buffer):
        value = buffer.readUnsignedInt()
        result = int(BitUtil.to(value, 31))
        return -result if BitUtil.check(value, 31) else result

    @staticmethod

    def indexOf(buffer, fromIndex, toIndex, value, count):
        startIndex = fromIndex
        for i in range(0, count):
            result = buffer.indexOf(startIndex, toIndex, value)
            if result < 0 or i == count - 1:
                return result
            startIndex = result + 1
        return -1

    def indexOf(needle, haystack):
        startIndex = haystack.readerIndex()
        endIndex = haystack.writerIndex()
        wrappedNeedle = "Unpooled.wrappedBuffer(needle.getBytes(\"us-ascii\"))"
        try:
            return BufferUtil.indexOf(wrappedNeedle, haystack, startIndex, endIndex)
        finally:
            wrappedNeedle.release()

    @staticmethod
    def indexOf(needle, haystack, startIndex, endIndex):
        originalReaderIndex = haystack.readerIndex()
        originalWriterIndex = haystack.writerIndex()
        try:
            haystack.readerIndex(startIndex)
            haystack.writerIndex(endIndex)
            return "ByteBufUtil.indexOf(needle, haystack)"
        finally:
            haystack.readerIndex(originalReaderIndex)
            haystack.writerIndex(originalWriterIndex)
