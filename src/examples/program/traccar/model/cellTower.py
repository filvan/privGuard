from src.examples.program.traccar.config.config import Keys


class CellTower:

    def __init__(self):

        self._radioType = None
        self._cellId = 0
        self._locationAreaCode = 0
        self._mobileCountryCode = 0
        self._mobileNetworkCode = 0
        self._signalStrength = 0

    @staticmethod
    def from_(mcc, mnc, lac, cid):
        cellTower = CellTower()
        cellTower.setMobileCountryCode(mcc)
        cellTower.setMobileNetworkCode(mnc)
        cellTower.setLocationAreaCode(lac)
        cellTower.setCellId(cid)
        return cellTower

    @staticmethod
    def from_(mcc, mnc, lac, cid, rssi):
        cellTower = CellTower.from_(mcc, mnc, lac, cid)
        cellTower.setSignalStrength(rssi)
        return cellTower

    @staticmethod
    def fromLacCid(config, lac, cid):
        return CellTower.from_(config.getInteger(Keys.GEOLOCATION_MCC), config.getInteger(Keys.GEOLOCATION_MNC), lac,
                               cid)

    @staticmethod
    def fromCidLac(config, cid, lac):
        return CellTower.fromLacCid(config, lac, cid)

    def getRadioType(self):
        return self._radioType

    def setRadioType(self, radioType):
        self._radioType = radioType

    def getCellId(self):
        return self._cellId

    def setCellId(self, cellId):
        self._cellId = cellId

    def getLocationAreaCode(self):
        return self._locationAreaCode

    def setLocationAreaCode(self, locationAreaCode):
        self._locationAreaCode = locationAreaCode

    def getMobileCountryCode(self):
        return self._mobileCountryCode

    def setMobileCountryCode(self, mobileCountryCode):
        self._mobileCountryCode = mobileCountryCode

    def getMobileNetworkCode(self):
        return self._mobileNetworkCode

    def setMobileNetworkCode(self, mobileNetworkCode):
        self._mobileNetworkCode = mobileNetworkCode

    def getSignalStrength(self):
        return self._signalStrength

    def setSignalStrength(self, signalStrength):
        self._signalStrength = signalStrength

    def setOperator(self, operator):
        operatorString = str(operator)
        self._mobileCountryCode = int(operatorString[0:3])
        self._mobileNetworkCode = int(operatorString[3:])

    def equals(self, o):
        if self is o:
            return True
        if o is None or self.__class__ != type(o):
            return False
        cellTower = o
        return self._radioType == cellTower._radioType and self._cellId == cellTower._cellId and self._locationAreaCode == cellTower._locationAreaCode and self._mobileCountryCode == cellTower._mobileCountryCode and self._mobileNetworkCode == cellTower._mobileNetworkCode and self._signalStrength == cellTower._signalStrength
