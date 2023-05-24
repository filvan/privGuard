class BaseReportItem:

    def __init__(self):
        self._deviceId = 0
        self._deviceName = None
        self._distance = 0
        self._averageSpeed = 0
        self._maxSpeed = 0
        self._spentFuel = 0
        self._startOdometer = 0
        self._endOdometer = 0
        self._startTime = None
        self._endTime = None



    def getDeviceId(self):
        return self._deviceId

    def setDeviceId(self, deviceId):
        self._deviceId = deviceId


    def getDeviceName(self):
        return self._deviceName

    def setDeviceName(self, deviceName):
        self._deviceName = deviceName


    def getDistance(self):
        return self._distance

    def setDistance(self, distance):
        self._distance = distance

    def addDistance(self, distance):
        self._distance += distance


    def getAverageSpeed(self):
        return self._averageSpeed

    def setAverageSpeed(self, averageSpeed):
        self._averageSpeed = averageSpeed


    def getMaxSpeed(self):
        return self._maxSpeed

    def setMaxSpeed(self, maxSpeed):
        self._maxSpeed = maxSpeed


    def getSpentFuel(self):
        return self._spentFuel

    def setSpentFuel(self, spentFuel):
        self._spentFuel = spentFuel


    def getStartOdometer(self):
        return self._startOdometer

    def setStartOdometer(self, startOdometer):
        self._startOdometer = startOdometer

    def getEndOdometer(self):
        return self._endOdometer

    def setEndOdometer(self, endOdometer):
        self._endOdometer = endOdometer


    def getStartTime(self):
        return self._startTime

    def setStartTime(self, startTime):
        self._startTime = startTime


    def getEndTime(self):
        return self._endTime

    def setEndTime(self, endTime):
        self._endTime = endTime
