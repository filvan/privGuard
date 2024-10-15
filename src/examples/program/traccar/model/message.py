from .extendedModel import ExtendedModel


class Message(ExtendedModel):

    def __init__(self):
        # instance fields found by Java to Python Converter:
        super().__init__()
        self._deviceId = 0
        self._type = None

    def getDeviceId(self):
        return self._deviceId

    def setDeviceId(self, deviceId):
        self._deviceId = deviceId

    def getType(self):
        return self._type

    def setType(self, type):
        self._type = type
