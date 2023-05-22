from datetime import timezone, date
from enum import Enum

from src.examples.program.traccar.helper.dateBuilder import DateBuilder


class Parser:


    def __init__(self, pattern, input):

        self._position = 0
        self._matcher = None

        self._matcher = pattern.matcher(input)

    def matches(self):
        self._position = 1
        return self._matcher.matches()

    def find(self):
        self._position = 1
        return self._matcher.find()

    def skip(self, number):
        self._position += number


    def hasNext(self):
        return self.hasNext(1)


    def hasNext(self, number):
        i = self._position
        while i < self._position + number:
            value = self._matcher.group(i)
            if value is None or not value:
                self._position += number
                return False
            i += 1
        return True

    def hasNextAny(self, number):
        i = self._position
        while i < self._position + number:
            value = self._matcher.group(i)
            if value is not None and value:
                return True
            i += 1
        self._position += number
        return False

    def next(self):

        temp_var = self._matcher.group(self._position)
        self._position += 1
        return temp_var


    def nextInt(self):
        if self.hasNext():
            return int(self.next())
        else:
            return None


    def nextInt(self, defaultValue):
        if self.hasNext():
            return int(self.next())
        else:
            return defaultValue


    def nextHexInt(self):
        if self.hasNext():
            return int.parseInt(self.next(), 16)
        else:
            return None


    def nextHexInt(self, defaultValue):
        if self.hasNext():
            return int.parseInt(self.next(), 16)
        else:
            return defaultValue


    def nextBinInt(self):
        if self.hasNext():
            return int.parseInt(self.next(), 2)
        else:
            return None


    def nextBinInt(self, defaultValue):
        if self.hasNext():
            return int.parseInt(self.next(), 2)
        else:
            return defaultValue


    def nextLong(self):
        if self.hasNext():
            return int(self.next())
        else:
            return None

    def nextHexLong(self):
        if self.hasNext():
            return int.parseLong(self.next(), 16)
        else:
            return None


    def nextLong(self, defaultValue):
        return self.nextLong(10, defaultValue)


    def nextLong(self, radix, defaultValue):
        if self.hasNext():
            return int.parseLong(self.next(), radix)
        else:
            return defaultValue


    def nextDouble(self):
        if self.hasNext():
            return float(self.next())
        else:
            return None


    def nextDouble(self, defaultValue):
        if self.hasNext():
            return float(self.next())
        else:
            return defaultValue

    from enum import Enum

    class CoordinateFormat(Enum):
        DEG_DEG = 0
        DEG_DEG_HEM = 1
        DEG_HEM = 2
        DEG_MIN_MIN = 3
        DEG_MIN_HEM = 4
        DEG_MIN_MIN_HEM = 5
        HEM_DEG_MIN_MIN = 6
        HEM_DEG = 7
        HEM_DEG_MIN = 8
        HEM_DEG_MIN_HEM = 9


    def nextCoordinate(self, format):
        coordinate = 0
        hemisphere = None

        if format == self.CoordinateFormat.DEG_DEG:
            coordinate = float(next() + '.' + next())
        elif format == self.CoordinateFormat.DEG_DEG_HEM:
            coordinate = float(next() + '.' + next())
            hemisphere = next()
        elif format == self.CoordinateFormat.DEG_HEM:
            coordinate = self.nextDouble(0)
            hemisphere = next()
        elif format == self.CoordinateFormat.DEG_MIN_MIN:
            coordinate = self.nextInt(0)
            coordinate += float(next() + '.' + next()) / 60
        elif format == self.CoordinateFormat.DEG_MIN_MIN_HEM:
            coordinate = self.nextInt(0)
            coordinate += float(next() + '.' + next()) / 60
            hemisphere = next()
        elif format == self.CoordinateFormat.HEM_DEG:
            hemisphere = next()
            coordinate = self.nextDouble(0)
        elif format == self.CoordinateFormat.HEM_DEG_MIN:
            hemisphere = next()
            coordinate = self.nextInt(0)

            coordinate += self.nextDouble(0) / 60
        elif format == self.CoordinateFormat.HEM_DEG_MIN_HEM:
            hemisphere = next()
            coordinate = self.nextInt(0)

            coordinate += self.nextDouble(0) / 60
            if self.hasNext():
                hemisphere = next()
        elif format == self.CoordinateFormat.HEM_DEG_MIN_MIN:
            hemisphere = next()
            coordinate = self.nextInt(0)
            coordinate += float(next() + '.' + next()) / 60
        else:
            coordinate = self.nextInt(0)

            coordinate += self.nextDouble(0) / 60
            hemisphere = next()

        if hemisphere is not None and (hemisphere == "S" or hemisphere == "W" or hemisphere == "-"):
            coordinate = -abs(coordinate)

        return coordinate


    def nextCoordinate(self):
        return self.nextCoordinate(self.CoordinateFormat.DEG_MIN_HEM)

    class DateTimeFormat(Enum):
        HMS = 0
        SMH = 1
        HMS_YMD = 2
        HMS_DMY = 3
        SMH_YMD = 4
        SMH_DMY = 5
        DMY_HMS = 6
        DMY_HMSS = 7
        YMD_HMS = 8
        YMD_HMSS = 9


    def nextDateTime(self, format, timeZone):
        year = 0
        month = 0
        day = 0
        hour = 0
        minute = 0
        second = 0
        millisecond = 0

        if format is self.HMS:
            hour = self.nextInt(0)
            minute = self.nextInt(0)
            second = self.nextInt(0)
        elif format is self.SMH:
            second = self.nextInt(0)
            minute = self.nextInt(0)
            hour = self.nextInt(0)
        elif format is self.HMS_YMD:
            hour = self.nextInt(0)
            minute = self.nextInt(0)
            second = self.nextInt(0)
            year = self.nextInt(0)
            month = self.nextInt(0)
            day = self.nextInt(0)
        elif format is self.HMS_DMY:
            hour = self.nextInt(0)
            minute = self.nextInt(0)
            second = self.nextInt(0)
            day = self.nextInt(0)
            month = self.nextInt(0)
            year = self.nextInt(0)
        elif format is self.SMH_YMD:
            second = self.nextInt(0)
            minute = self.nextInt(0)
            hour = self.nextInt(0)
            year = self.nextInt(0)
            month = self.nextInt(0)
            day = self.nextInt(0)
        elif format is self.SMH_DMY:
            second = self.nextInt(0)
            minute = self.nextInt(0)
            hour = self.nextInt(0)
            day = self.nextInt(0)
            month = self.nextInt(0)
            year = self.nextInt(0)
        elif (format is self.DMY_HMS) or (format is self.DMY_HMSS):
            day = self.nextInt(0)
            month = self.nextInt(0)
            year = self.nextInt(0)
            hour = self.nextInt(0)
            minute = self.nextInt(0)
            second = self.nextInt(0)

        if format != self.HMS and format != self.SMH and format != self.HMS_YMD and format != self.HMS_DMY and format != self.SMH_YMD and format != self.SMH_DMY and format != self.DMY_HMS and format != self.DMY_HMSS:
            year = self.nextInt(0)
            month = self.nextInt(0)
            day = self.nextInt(0)
            hour = self.nextInt(0)
            minute = self.nextInt(0)
            second = self.nextInt(0)

        if format is self.DateTimeFormat.YMD_HMSS or format is self.DateTimeFormat.DMY_HMSS:
            millisecond = self.nextInt(0)

        if year >= 0 and year < 100:
            year += 2000

        dateBuilder = None
        if format is not self.DateTimeFormat.HMS and format is not self.DateTimeFormat.SMH:
            if timeZone is not None:
                dateBuilder = DateBuilder(timezone.getTimeZone(timeZone))
            else:
                dateBuilder = DateBuilder()
            dateBuilder.setDate(year, month, day)
        else:
            if timeZone is not None:
                dateBuilder = DateBuilder(date(), timezone.getTimeZone(timeZone))
            else:
                dateBuilder = DateBuilder(date())

        dateBuilder.setTime(hour, minute, second, millisecond)

        return dateBuilder.getDate()


    def nextDateTime(self, format):
        return self.nextDateTime(format, None)


    def nextDateTime(self):
        return self.nextDateTime(self.DateTimeFormat.YMD_HMS, None)


