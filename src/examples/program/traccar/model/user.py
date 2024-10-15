from src.examples.program.traccar.helper.hashing import Hashing
from src.examples.program.traccar.storage.queryIgnore import QueryIgnore
from src.examples.program.traccar.storage.storageName import StorageName
from .extendedModel import ExtendedModel
from .disableable import Disableable
from .userRestriction import UserRestrictions


class User(ExtendedModel, UserRestrictions, Disableable):

    def __init__(self):
        super().__init__()
        self._name = None
        self._login = None
        self._email = None
        self._phone = None
        self._readonly = False
        self._administrator = False
        self._map = None
        self._latitude = 0
        self._longitude = 0
        self._zoom = 0
        self._twelveHourFormat = False
        self._coordinateFormat = None
        self._disabled = False
        self._expirationTime = None
        self._deviceLimit = 0
        self._userLimit = 0
        self._deviceReadonly = False
        self._limitCommands = False
        self._disableReports = False
        self._fixedEmail = False
        self._poiLayer = None
        self._hashedPassword = None
        self._salt = None

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getLogin(self):
        return self._login

    def setLogin(self, login):
        self._login = login

    def getEmail(self):
        return self._email

    def setEmail(self, email):
        self._email = email.trim()

    def getPhone(self):
        return self._phone

    def setPhone(self, phone):
        self._phone = phone

    def getReadonly(self):
        return self._readonly

    def setReadonly(self, readonly):
        self._readonly = readonly

    def getManager(self):
        return self._userLimit != 0

    def getAdministrator(self):
        return self._administrator

    def setAdministrator(self, administrator):
        self._administrator = administrator

    def getMap(self):
        return self._map

    def setMap(self, map):
        self._map = map

    def getLatitude(self):
        return self._latitude

    def setLatitude(self, latitude):
        self._latitude = latitude

    def getLongitude(self):
        return self._longitude

    def setLongitude(self, longitude):
        self._longitude = longitude

    def getZoom(self):
        return self._zoom

    def setZoom(self, zoom):
        self._zoom = zoom

    def getTwelveHourFormat(self):
        return self._twelveHourFormat

    def setTwelveHourFormat(self, twelveHourFormat):
        self._twelveHourFormat = twelveHourFormat

    def getCoordinateFormat(self):
        return self._coordinateFormat

    def setCoordinateFormat(self, coordinateFormat):
        self._coordinateFormat = coordinateFormat

    def getDisabled(self):
        return self._disabled

    def setDisabled(self, disabled):
        self._disabled = disabled

    def getExpirationTime(self):
        return self._expirationTime

    def setExpirationTime(self, expirationTime):
        self._expirationTime = expirationTime

    def getDeviceLimit(self):
        return self._deviceLimit

    def setDeviceLimit(self, deviceLimit):
        self._deviceLimit = deviceLimit

    def getUserLimit(self):
        return self._userLimit

    def setUserLimit(self, userLimit):
        self._userLimit = userLimit

    def getDeviceReadonly(self):
        return self._deviceReadonly

    def setDeviceReadonly(self, deviceReadonly):
        self._deviceReadonly = deviceReadonly

    def getLimitCommands(self):
        return self._limitCommands

    def setLimitCommands(self, limitCommands):
        self._limitCommands = limitCommands

    def getDisableReports(self):
        return self._disableReports

    def setDisableReports(self, disableReports):
        self.disableReports = disableReports

    def getFixedEmail(self):
        return self._fixedEmail

    def setFixedEmail(self, fixedEmail):
        self._fixedEmail = fixedEmail

    def getPoiLayer(self):
        return self._poiLayer

    def setPoiLayer(self, poiLayer):
        self._poiLayer = poiLayer

    def getPassword(self):
        return None

    def setPassword(self, password):
        if password is not None and password:
            hashingResult = Hashing.createHash(password)
            self._hashedPassword = hashingResult.getHash()
            self._salt = hashingResult.getSalt()

    def getHashedPassword(self):
        return self._hashedPassword

    def setHashedPassword(self, hashedPassword):
        self._hashedPassword = hashedPassword

    def getSalt(self):
        return self._salt

    def setSalt(self, salt):
        self._salt = salt

    def isPasswordValid(self, password):
        return Hashing.validatePassword(password, self._hashedPassword, self._salt)
