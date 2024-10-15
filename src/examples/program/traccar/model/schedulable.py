from .extendedModel import ExtendedModel


class Schedulable(ExtendedModel):

    def __init__(self):
        # instance fields found by Java to Python Converter:
        super().__init__()
        self._calendarId = 0

    def getCalendarId(self):
        return self._calendarId

    def setCalendarId(self, calendarId):
        self._calendarId = calendarId
