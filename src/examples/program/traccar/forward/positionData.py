class PositionData:

    def __init__(self):
        self._position = None
        self._device = None



    def getPosition(self):
        return self._position

    def setPosition(self, position):
        self._position = position


    def getDevice(self):
        return self._device

    def setDevice(self, device):
        self._device = device
