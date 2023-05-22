class BitBuffer:

    def _initialize_instance_fields(self):

        self._buffer = None
        self._writeByte = 0
        self._writeCount = 0
        self._readByte = 0
        self._readCount = 0







    def __init__(self):
        self._initialize_instance_fields()

        self._buffer = "Unpooled.buffer()"



    def __init__(self, buffer):
        self._initialize_instance_fields()

        self._buffer = buffer

    def writeEncoded(self, bytes):
        for b in bytes:
            b -= 48
            if b > 40:
                b -= 8
            self.write(b)

    def write(self, b):
        if self._writeCount == 0:
            self._writeByte |= b
            self._writeCount = 6
        else:
            remaining = 8 - self._writeCount
            self._writeByte <<= remaining
            self._writeByte |= b >> (6 - remaining)
            self._buffer.writeByte(self._writeByte)
            self._writeByte = b & ((1 << (6 - remaining)) - 1)
            self._writeCount = 6 - remaining

    def readUnsigned(self, length):
        result = 0

        while length > 0:
            if self._readCount == 0:
                self._readByte = self._buffer.readUnsignedByte()
                self._readCount = 8
            if self._readCount >= length:
                result <<= length
                result |= self._readByte >> (self._readCount - length)
                self._readByte &= (1 << (self._readCount - length)) - 1
                self._readCount -= length
                length = 0
            else:
                result <<= self._readCount
                result |= self._readByte
                length -= self._readCount
                self._readByte = 0
                self._readCount = 0

        return result

    def readSigned(self, length):
        result = self.readUnsigned(length)
        signBit = 1 << (length - 1)
        if (result & signBit) == 0:
            return result
        else:
            result &= signBit - 1
            result += -signBit
            return result
