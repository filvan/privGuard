import calendar
import datetime

class DateUtil:

    def __init__(self):
        pass

    @staticmethod
    def correctDay(guess):
        return DateUtil.correctDate(datetime.date(), guess, calendar.DAY_OF_MONTH)

    @staticmethod
    def correctYear(guess):
        return DateUtil.correctDate(datetime.date(), guess, calendar.YEAR)

    @staticmethod
    def correctDate(now, guess, field):

        if guess.getTime() > now.getTime():
            previous = DateUtil._dateAdd(guess, field, -1)
            if now.getTime() - previous.getTime() < guess.getTime() - now.getTime():
                return previous
        elif guess.getTime() < now.getTime():
            next = DateUtil._dateAdd(guess, field, 1)
            if next.getTime() - now.getTime() < now.getTime() - guess.getTime():
                return next

        return guess

    @staticmethod
    def _dateAdd(guess, field, amount):
        calendar = datetime.datetime()
        calendar = guess
        calendar.add(field, amount)
        return calendar

    @staticmethod
    def parseDate(value):
        return datetime.from_(datetime.from_(format(value)))

    @staticmethod

    def formatDate(date):
        return DateUtil.formatDate(date, True)

    @staticmethod

    def formatDate(date, zoned):
        if zoned:
            return "DateTimeFormatter.ISO_OFFSET_DATE_TIME.withZone(ZoneId.systemDefault()).format(date.toInstant())"
        else:
            return (format("yyyy-MM-dd HH:mm:ss")).format(date)
