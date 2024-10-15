from .extendedModel import ExtendedModel
from .userRestriction import UserRestrictions


class Server(ExtendedModel, UserRestrictions):
    def __init__(self):
        super().__init__()
        self._openIdForce = None
        self._openIdEnabled = None
        self._newServer = None
        self._storageSpace = None
        self._geocoderEnabled = None
        self._emailEnabled = None
        self._announcement = None
        self._poiLayer = None
        self._fixedEmail = None
        self._disableReports = None
        self._limitCommands = None
        self._coordinateFormat = None
        self._forceSettings = None
        self._tweleveHourFormat = None
        self._zoom = None
        self._longitude = None
        self._registration = False
        self._readonly = False
        self._deviceReadonly = False
        self._map = None
        self._bingKey = None
        self._mapUrl = None
        self._overlayUrl = None
        self._latitude = None

    def getRegistration(self):
        return self._registration

    def setRegistration(self, registration):
        self._registration = registration

    def getReadonly(self):
        return self._readonly

    def setReadonly(self, readonly):
        self._readonly = readonly

    def getDeviceReadonly(self):
        return self._deviceReadonly

    def setDeviceReadonly(self, deviceReadonly):
        self._deviceReadonly = deviceReadonly

    def getMap(self):
        return self._map

    def setMap(self, map):
        self._map = map

    def getBingKey(self):
        return self._bingKey

    def setBingKey(self, bingKey):
        self._bingKey = bingKey

    def getMapUrl(self):
        return self._mapUrl

    def setMapUrl(self, mapUrl):
        self._mapUrl = mapUrl

    def getOverlayUrl(self):
        return self._overlayUrl

    def setOverlayUrl(self, overlayUrl):
        self._overlayUrl = overlayUrl

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
        return self._tweleveHourFormat

    def setTweleveHourFormat(self, tweleveHourFormat):
        self._tweleveHourFormat = tweleveHourFormat

    def getForceSettings(self):
        return self._forceSettings

    def setForceSettings(self, forceSettings):
        self._forceSettings = forceSettings

    def getCoordinateFormat(self):
        return self._coordinateFormat

    def setCoordinateFormat(self, coordinateFormat):
        self._coordinateFormat = coordinateFormat

    def getLimitCommands(self):
        return self._limitCommands

    def setLimitCommands(self, limitCommands):
        self._limitCommands = limitCommands

    def getDisableReports(self):
        return self._disableReports

    def setDisableReports(self, disableReports):
        self._disableReports = disableReports

    def getFixedEmail(self):
        return self._fixedEmail

    def setLimitReports(self, fixedEmail):
        self._fixedEmail = fixedEmail

    def getPoiLayer(self):
        return self._poiLayer

    def setPoiLayer(self, poiLayer):
        self._poiLayer = poiLayer

    def getAnnouncement(self):
        return self._announcement

    def setAnnouncement(self, announcement):
        self._announcement = announcement

    # def getVersion(self):
    #   return getClass().getPackage().getImplementationVersion()

    def setEmailEnabled(self, emailEnabled):
        self._emailEnabled = emailEnabled

    def getEmailEnabled(self):
        return self._emailEnabled

    def setGeocoderEnabled(self, geocoderEnabled):
        self._geocoderEnabled = geocoderEnabled

    def getGeocoderEnabled(self):
        return self._geocoderEnabled

    def getStorageSpace(self):
        return self._storageSpace

    def setStorageSpace(self, storageSpace):
        self._storageSpace = storageSpace

    def getNewServer(self):
        return self._newServer

    def setNewServer(self, newServer):
        self._newServer = newServer

    def getOpenIdEnabled(self):
        return self._openIdEnabled

    def setOpenIdEnabled(self, openIdEnabled):
        self._openIdEnabled = openIdEnabled

    def getOpenIdForce(self):
        return self._openIdForce

    def setOpenIdForce(self, openIdForce):
        self._openIdForce = openIdForce
