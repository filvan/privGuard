from .extendedModel import ExtendedModel


class Maintenance(ExtendedModel):

    def __init__(self):
        # instance fields found by Java to Python Converter:
        super().__init__()
        self._name = None
        self._type = None
        self._start = 0
        self._period = 0

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getType(self):
        return self._type

    def setType(self, type):
        self._type = type

    def getStart(self):
        return self._start

    def setStart(self, start):
        self._start = start

    def getPeriod(self):
        return self._period

    def setPeriod(self, period):
        self._period = period
