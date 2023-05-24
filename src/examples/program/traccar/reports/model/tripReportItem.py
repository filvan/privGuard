from src.examples.program.traccar.reports.model.baseReportItem import BaseReportItem


class TripReportItem(BaseReportItem):

    def __init__(self):
        #instance fields found by Java to Python Converter:
        self._startPositionId = 0
        self._endPositionId = 0
        self._startLat = 0
        self._startLon = 0
        self._endLat = 0
        self._endLon = 0
        self._startAddress = None
        self._endAddress = None
        self._duration = 0
        self._driverUniqueId = None
        self._driverName = None



    def getStartPositionId(self):
        return self._startPositionId

    def setStartPositionId(self, startPositionId):
        self._startPositionId = startPositionId


    def getEndPositionId(self):
        return self._endPositionId

    def setEndPositionId(self, endPositionId):
        self._endPositionId = endPositionId


    def getStartLat(self):
        return self._startLat

    def setStartLat(self, startLat):
        self._startLat = startLat


    def getStartLon(self):
        return self._startLon

    def setStartLon(self, startLon):
        self._startLon = startLon


    def getEndLat(self):
        return self._endLat

    def setEndLat(self, endLat):
        self._endLat = endLat


    def getEndLon(self):
        return self._endLon

    def setEndLon(self, endLon):
        self._endLon = endLon


    def getStartAddress(self):
        return self._startAddress

    def setStartAddress(self, address):
        self._startAddress = address


    def getEndAddress(self):
        return self._endAddress

    def setEndAddress(self, address):
        self._endAddress = address


    def getDuration(self):
        return self._duration

    def setDuration(self, duration):
        self._duration = duration


    def getDriverUniqueId(self):
        return self._driverUniqueId

    def setDriverUniqueId(self, driverUniqueId):
        self._driverUniqueId = driverUniqueId


    def getDriverName(self):
        return self._driverName

    def setDriverName(self, driverName):
        self._driverName = driverName
