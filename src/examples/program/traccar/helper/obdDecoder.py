from collections import OrderedDict

from src.examples.program.traccar.model.position import Position

import math

class ObdDecoder:

    def __init__(self):
        pass

    _MODE_CURRENT = 0x01
    _MODE_FREEZE_FRAME = 0x02
    _MODE_CODES = 0x03

    @staticmethod
    def decode(mode, value):
        if (mode == ObdDecoder._MODE_CURRENT) or (mode == ObdDecoder._MODE_FREEZE_FRAME):
            return ObdDecoder.decodeData(int.parseInt(value[0:2], 16), int.parseLong(value[2:], 16), True)
        elif mode == ObdDecoder._MODE_CODES:
            return ObdDecoder.decodeCodes(value)
        else:
            return None

    @staticmethod
    def _createEntry(key, value):
        return OrderedDict.__setitem__(key, value)

    @staticmethod
    def decodeCodes(value):
        codes = ""
        i = 0
        while i < math.trunc(len(value) / float(4)):
            numValue = int.parseInt(value[i * 4:(i + 1) * 4], 16)
            codes+= (' ')
            if (numValue >> 14) == 1:
                codes += ('C')
            elif (numValue >> 14) == 2:
                codes += ('B')
            elif (numValue >> 14) == 3:
                codes += ('U')
            else:
                codes += ('P')
            codes += ("{0:0>4X}".format(numValue & 0x3FFF))
            i += 1
        if codes.length() > 0:
            return ObdDecoder._createEntry(Position.KEY_DTCS, str(codes).trim())
        else:
            return None

    @staticmethod
    def decodeData(pid, value, convert):
        if pid == 0x04:
            return ObdDecoder._createEntry(Position.KEY_ENGINE_LOAD,math.trunc(value * 100 / float(255)) if convert else value)
        elif pid == 0x05:
            return ObdDecoder._createEntry(Position.KEY_COOLANT_TEMP,value - 40 if convert else value)
        elif pid == 0x0B:
            return ObdDecoder._createEntry("mapIntake", value)
        elif pid == 0x0C:
            return ObdDecoder._createEntry(Position.KEY_RPM,math.trunc(value / float(4)) if convert else value)
        elif pid == 0x0D:
            return ObdDecoder._createEntry(Position.KEY_OBD_SPEED, value)
        elif pid == 0x0F:
            return ObdDecoder._createEntry("intakeTemp",value - 40 if convert else value)
        elif pid == 0x11:
            return ObdDecoder._createEntry(Position.KEY_THROTTLE,math.trunc(value * 100 / float(255)) if convert else value)
        elif pid == 0x21:
            return ObdDecoder._createEntry("milDistance", value)
        elif pid == 0x2F:
            return ObdDecoder._createEntry(Position.KEY_FUEL_LEVEL,math.trunc(value * 100 / float(255)) if convert else value)
        elif pid == 0x31:
            return ObdDecoder._createEntry("clearedDistance", value)
        else:
            return None
