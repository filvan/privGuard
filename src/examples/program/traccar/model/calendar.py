from collections import OrderedDict

from numpy import array

from .extendedModel import ExtendedModel

class Calendar(ExtendedModel):

    def __init__(self):

        self._name = None
        self._data = None
        self._calendar = None



    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name


    def getData(self):
        return self._data

    def setData(self, data):
        builder = OrderedDict()
        self._calendar = builder.build(data)
        self._data = data


    def getCalendar(self):
        return self._calendar

    def _findEvents(self, date):
        if self._calendar is not None:
            filter = "Filter(PeriodRule(Period(DateTime(date), Duration.ZERO)))"
            return filter.filter(self._calendar.getComponents("CalendarComponent.VEVENT"))
        else:
            return array()

    def findPeriods(self, date):
        calendarDate = date(date)
        return self._findEvents(date).stream().flatMap(lambda event : event.getConsumedTime(calendarDate, calendarDate).stream()).collect(array())

    def checkMoment(self, date):
        return self._findEvents(date)
