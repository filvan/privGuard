import math

class BcdUtil:

    def __init__(self):
        pass

    @staticmethod
    def readInteger(buf, digits):
        result = 0

        i = 0
        while i < math.trunc(digits / float(2)):
            b = buf.readUnsignedByte()
            result *= 10
            result += b #>>> 4
            result *= 10
            result += b & 0x0f
            i += 1

        if math.fmod(digits, 2) != 0:
            b = buf.getUnsignedByte(buf.readerIndex())
            result *= 10
            result += b #>>> 4

        return result

    @staticmethod
    def readCoordinate(buf):
        b1 = buf.readUnsignedByte()
        b2 = buf.readUnsignedByte()
        b3 = buf.readUnsignedByte()
        b4 = buf.readUnsignedByte()

        value = (b2 & 0xf) * 10 + (b3 >> 4)
        value += (((b3 & 0xf) * 10 + (b4 >> 4)) * 10 + (b4 & 0xf)) / 1000.0
        value /= 60
        value += ((b1 >> 4 & 0x7) * 10 + (b1 & 0xf)) * 10 + (b2 >> 4)

        if (b1 & 0x80) != 0:
            value = -value

        return value
