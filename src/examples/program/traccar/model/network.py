class Network:

    def _initialize_instance_fields(self):
        #instance fields found by Java to Python Converter:
        self._homeMobileCountryCode = 0
        self._homeMobileNetworkCode = 0
        self._radioType = "gsm"
        self._carrier = None
        self._considerIp = False
        self._cellTowers = None
        self._wifiAccessPoints = None


#JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
#ORIGINAL LINE: public Network()
    def __init__(self):
        self._initialize_instance_fields()


#JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
#ORIGINAL LINE: public Network(CellTower cellTower)
    def __init__(self, cellTower):
        self._initialize_instance_fields()

        self.addCellTower(cellTower)

#JAVA TO PYTHON CONVERTER TASK: There is no Python equivalent to multiple constructors:
#ORIGINAL LINE: public Network(WifiAccessPoint wifiAccessPoint)
    def __init__(self, wifiAccessPoint):
        self._initialize_instance_fields()

        self.addWifiAccessPoint(wifiAccessPoint)


    def getHomeMobileCountryCode(self):
        return self._homeMobileCountryCode

    def setHomeMobileCountryCode(self, homeMobileCountryCode):
        self._homeMobileCountryCode = homeMobileCountryCode


    def getHomeMobileNetworkCode(self):
        return self._homeMobileNetworkCode

    def setHomeMobileNetworkCode(self, homeMobileNetworkCode):
        self._homeMobileNetworkCode = homeMobileNetworkCode


    def getRadioType(self):
        return self._radioType

    def setRadioType(self, radioType):
        self._radioType = radioType


    def getCarrier(self):
        return self._carrier

    def setCarrier(self, carrier):
        self._carrier = carrier


    def getConsiderIp(self):
        return self._considerIp

    def setConsiderIp(self, considerIp):
        self._considerIp = considerIp


    def getCellTowers(self):
        return self._cellTowers

    def setCellTowers(self, cellTowers):
        self._cellTowers = cellTowers

    def addCellTower(self, cellTower):
        if self._cellTowers is None:
            self._cellTowers = []
        self._cellTowers.add(cellTower)


    def getWifiAccessPoints(self):
        return self._wifiAccessPoints

    def setWifiAccessPoints(self, wifiAccessPoints):
        self._wifiAccessPoints = wifiAccessPoints

    def addWifiAccessPoint(self, wifiAccessPoint):
        if self._wifiAccessPoints is None:
            self._wifiAccessPoints = []
        self._wifiAccessPoints.add(wifiAccessPoint)

    def equals(self, o):
        if self is o:
            return True
        if o is None or self.__class__ != type(o):
            return False
        network = o
        return self._homeMobileCountryCode == network._homeMobileCountryCode and self._homeMobileNetworkCode == network._homeMobileNetworkCode and self._radioType == network._radioType and self._carrier == network._carrier and self._cellTowers == network._cellTowers and self._wifiAccessPoints == network._wifiAccessPoints

