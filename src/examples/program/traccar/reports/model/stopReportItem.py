from src.examples.program.traccar.reports.model.baseReportItem import BaseReportItem


class StopReportItem(BaseReportItem):

    def __init__(self):
        self._positionId = 0
        self._latitude = 0
        self._longitude = 0
        self._address = None
        self._duration = 0
        self._engineHours = 0



    def getPositionId(self):
        return self._positionId

    def setPositionId(self, positionId):
        self._positionId = positionId


    def getLatitude(self):
        return self._latitude

    def setLatitude(self, latitude):
        self._latitude = latitude


    def getLongitude(self):
        return self._longitude

    def setLongitude(self, longitude):
        self._longitude = longitude


    def getAddress(self):
        return self._address

    def setAddress(self, address):
        self._address = address


    def getDuration(self):
        return self._duration

    def setDuration(self, duration):
        self._duration = duration


    def getEngineHours(self):
        return self._engineHours

    def setEngineHours(self, engineHours):
        self._engineHours = engineHours
