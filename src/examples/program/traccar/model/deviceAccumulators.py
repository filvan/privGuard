class DeviceAccumulators:

    def __init__(self):
        # instance fields found by Java to Python Converter:
        self._deviceId = 0
        self._totalDistance = 0
        self._hours = 0

    def getDeviceId(self):
        return self._deviceId

    def setDeviceId(self, deviceId):
        self._deviceId = deviceId

    def getTotalDistance(self):
        return self._totalDistance

    def setTotalDistance(self, totalDistance):
        self._totalDistance = totalDistance

    def getHours(self):
        return self._hours

    def setHours(self, hours):
        self._hours = hours
