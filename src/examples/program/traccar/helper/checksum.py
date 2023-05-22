
import math

class Checksum:

    def __init__(self):
        pass

    class Algorithm:


        def __init__(self, bits, poly, init, refIn, refOut, xorOut):

            self._poly = 0
            self._init = 0
            self._refIn = False
            self._refOut = False
            self._xorOut = 0
            self._table = None

            self._poly = poly
            self._init = init
            self._refIn = refIn
            self._refOut = refOut
            self._xorOut = xorOut
            self._table = self._initTable8() if bits == 8 else self._initTable16()

        def _initTable8(self):
            table = [0 for _ in range(256)]
            crc = 0
            for i in range(0, 256):
                crc = i
                for j in range(0, 8):
                    bit = (crc & 0x80) != 0
                    crc <<= 1
                    if bit:
                        crc ^= self._poly
                table[i] = crc & 0xFF
            return table

        def _initTable16(self):
            table = [0 for _ in range(256)]
            crc = 0
            for i in range(0, 256):
                crc = i << 8
                for j in range(0, 8):
                    bit = (crc & 0x8000) != 0
                    crc <<= 1
                    if bit:
                        crc ^= self._poly
                table[i] = crc & 0xFFFF
            return table


    @staticmethod
    def _reverse(value, bits):
        result = 0
        for i in range(0, bits):
            result = (result << 1) | (value & 1)
            value >>= 1
        return result

    @staticmethod
    def crc8(algorithm, buf):
        crc = algorithm.init
        while buf.hasRemaining():
            b = buf.get() & 0xFF
            if algorithm.refIn:
                b = Checksum._reverse(b, 8)
            crc = algorithm.table[(crc & 0xFF) ^ b]
        if algorithm.refOut:
            crc = Checksum._reverse(crc, 8)
        return (crc ^ algorithm.xorOut) & 0xFF

    @staticmethod
    def crc16(algorithm, buf):
        crc = algorithm.init
        while buf.hasRemaining():
            b = buf.get() & 0xFF
            if algorithm.refIn:
                b = Checksum._reverse(b, 8)
            crc = (crc << 8) ^ algorithm.table[((crc >> 8) & 0xFF) ^ b]
        if algorithm.refOut:
            crc = Checksum._reverse(crc, 16)
        return (crc ^ algorithm.xorOut) & 0xFFFF

    CRC8_EGTS = Algorithm(8, 0x31, 0xFF, False, False, 0x00)
    CRC8_ROHC = Algorithm(8, 0x07, 0xFF, True, True, 0x00)

    CRC16_IBM = Algorithm(16, 0x8005, 0x0000, True, True, 0x0000)
    CRC16_X25 = Algorithm(16, 0x1021, 0xFFFF, True, True, 0xFFFF)
    CRC16_MODBUS = Algorithm(16, 0x8005, 0xFFFF, True, True, 0x0000)
    CRC16_CCITT_FALSE = Algorithm(16, 0x1021, 0xFFFF, False, False, 0x0000)
    CRC16_KERMIT = Algorithm(16, 0x1021, 0x0000, True, True, 0x0000)
    CRC16_XMODEM = Algorithm(16, 0x1021, 0x0000, False, False, 0x0000)

    @staticmethod
    def crc32(buf):
        checksum = "CRC32()"
        while buf.hasRemaining():
            checksum.update(buf.get())
        return int(checksum.getValue())

    @staticmethod

    def xor(buf):
        checksum = 0
        while buf.hasRemaining():
            checksum ^= buf.get()
        return checksum

    @staticmethod

    def xor(string):
        checksum = 0
        for b in string.getBytes("us-ascii"):
            checksum ^= b
        return checksum

    @staticmethod
    def nmea(string):
        return "*{0:0>2X}".format(Checksum.xor(string))

    @staticmethod

    def sum(buf):
        checksum = 0
        while buf.hasRemaining():
            checksum += buf.get()
        return checksum

    @staticmethod
    def modulo256(buf):
        checksum = 0
        while buf.hasRemaining():
            checksum = (checksum + buf.get()) & 0xFF
        return checksum

    @staticmethod

    def sum(msg):
        checksum = 0
        for b in msg.getBytes("us-ascii"):
            checksum += b
        return "{0:0>2X}".format(checksum).toUpperCase()

    @staticmethod
    def luhn(imei):
        checksum = 0
        remain = imei

        i = 0
        while remain != 0:
            digit = math.fmod(remain, 10)

            if math.fmod(i, 2) == 0:
                digit *= 2
                if digit >= 10:
                    digit = 1 + (math.fmod(digit, 10))

            checksum += digit
            remain = math.trunc(remain / float(10))
            i += 1

        return math.fmod((10 - (math.fmod(checksum, 10))), 10)

    @staticmethod
    def ip(data):
        sum = 0
        while data.remaining() > 0:
            sum += data.get() & 0xff
            if (sum & 0x80000000) > 0:
                sum = (sum & 0xffff) + (sum >> 16)
        while (sum >> 16) > 0:
            sum = (sum & 0xffff) + sum >> 16
        sum = sum & 0xffff if (sum == 0xffff) else (~sum) & 0xffff
        return sum

