import calendar
import datetime

class DateBuilder:

    def _initialize_instance_fields(self):

        self._calendar = None



    def __init__(self):
        self(datetime.getTimeZone("UTC"))

    def __init__(self, time):
        self(time, datetime.getTimeZone("UTC"))

    def __init__(self, timeZone):
        self(datetime.datetime(), timeZone)

    def __init__(self, time, timeZone):
        self._initialize_instance_fields()

        self._calendar = calendar.getInstance(timeZone)
        self._calendar.clear()
        self._calendar.setTimeInMillis(time.getTime())

    def setYear(self, year):
        if year < 100:
            year += 2000
        self._calendar.set(calendar.YEAR, year)
        return self

    def setMonth(self, month):
        self._calendar.set(calendar.MONTH, month - 1)
        return self

    def setDay(self, day):
        self._calendar.set(calendar.DAY_OF_MONTH, day)
        return self

    def setDate(self, year, month, day):
        return self.setYear(year).setMonth(month).setDay(day)

    def setDateReverse(self, day, month, year):
        return self.setDate(year, month, day)

    def setCurrentDate(self):
        now = calendar.getInstance(self._calendar.getTimeZone())
        return self.setYear(now.year).setMonth(now.month + 1).setDay(now.day)

    def setHour(self, hour):
        self._calendar.set(calendar.HOUR_OF_DAY, hour)
        return self

    def setMinute(self, minute):
        self._calendar.set(calendar.MINUTE, minute)
        return self

    def addMinute(self, minute):
        self._calendar = self._calendar.replace(minute = self._calendar.minute + minute)
        return self

    def setSecond(self, second):
        self._calendar.set(calendar.SECOND, second)
        return self

    def addSeconds(self, seconds):
        self._calendar.setTimeInMillis(self._calendar.getTimeInMillis() + seconds * 1000)
        return self

    def setMillis(self, millis):
        self._calendar.set("Calendar.MILLISECOND", millis)
        return self

    def addMillis(self, millis):
        self._calendar.setTimeInMillis(self._calendar.getTimeInMillis() + millis)
        return self

    def setTime(self, hour, minute, second):
        return self.setHour(hour).setMinute(minute).setSecond(second)

    def setTimeReverse(self, second, minute, hour):
        return self.setHour(hour).setMinute(minute).setSecond(second)

    def setTime(self, hour, minute, second, millis):
        return self.setHour(hour).setMinute(minute).setSecond(second).setMillis(millis)

    def getDate(self):
        return self._calendar
