class WifiAccessPoint:

    def __init__(self):
        #instance fields found by Java to Python Converter:
        self._macAddress = None
        self._signalStrength = 0
        self._channel = 0


    @staticmethod
#JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def from_(macAddress, signalStrength):
        wifiAccessPoint = WifiAccessPoint()
        wifiAccessPoint.setMacAddress(macAddress)
        wifiAccessPoint.setSignalStrength(signalStrength)
        return wifiAccessPoint

    @staticmethod
#JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def from_(macAddress, signalStrength, channel):
        wifiAccessPoint = WifiAccessPoint.from_(macAddress, signalStrength)
        wifiAccessPoint.setChannel(channel)
        return wifiAccessPoint


    def getMacAddress(self):
        return self._macAddress

    def setMacAddress(self, macAddress):
        self._macAddress = macAddress


    def getSignalStrength(self):
        return self._signalStrength

    def setSignalStrength(self, signalStrength):
        self._signalStrength = signalStrength


    def getChannel(self):
        return self._channel

    def setChannel(self, channel):
        self._channel = channel

    def equals(self, o):
        if self is o:
            return True
        if o is None or o.__class__ != type(o):
            return False
        that = o
        return self._macAddress == that._macAddress and self._signalStrength == that._signalStrength and self._channel == that._channel


