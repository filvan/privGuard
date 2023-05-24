import collections
import json

from src.examples.program.traccar.database.statisticManager import StatisticsManager
from src.examples.program.traccar.geocoder.geocoder import Geocoder
from src.examples.program.traccar.geocoder.geocoderException import GeocoderException


class JsonGeocoder(Geocoder):

    _LOGGER = "LoggerFactory.getLogger(JsonGeocoder.class)"



    def __init__(self, client, url, cacheSize, addressFormat):

        self._client = None
        self._url = None
        self._addressFormat = None
        self._statisticsManager = None
        self._cache = None

        self._client = client
        self._url = url
        self._addressFormat = addressFormat
        if cacheSize > 0:
            self._cache = collections.synchronizedMap(self.LinkedHashMapAnonymousInnerClass(self, cacheSize))

    class LinkedHashMapAnonymousInnerClass(map()):


        def __init__(self, outerInstance, cacheSize):
            self._outerInstance = outerInstance
            self._cacheSize = cacheSize

        def removeEldestEntry(self, eldest):
            return self.size() > self._cacheSize

    def setStatisticsManager(self, statisticsManager):
        self._statisticsManager = statisticsManager

    def readValue(self, object, key):
        if object.containsKey(key) and not object.isNull(key):
            return object.getString(key)
        return None

    def _handleResponse(self, latitude, longitude, json, callback):

        address = self.parseAddress(json)
        if address is not None:
            formattedAddress = self._addressFormat.format(address)
            if self._cache is not None:
                self._cache[map().SimpleImmutableEntry(latitude, longitude)] = formattedAddress
            if callback is not None:
                callback.onSuccess(formattedAddress)
            return formattedAddress
        else:
            msg = "Empty address. Error: " + self.parseError(json)
            if callback is not None:
                callback.onFailure(GeocoderException(msg))
            else:
                JsonGeocoder._LOGGER.warn(msg)
        return None

    def getAddress(self, latitude, longitude, callback):

        if self._cache is not None:
            cachedAddress = self._cache[map.SimpleImmutableEntry(latitude, longitude)]
            if cachedAddress is not None:
                if callback is not None:
                    callback.onSuccess(cachedAddress)
                return cachedAddress

        if self._statisticsManager is not None:
            self._statisticsManager.registerGeocoderRequest()

        request = self._client.target(str.format(self._url, latitude, longitude)).request()

        if callback is not None:
            request.async_().get(self.InvocationCallbackAnonymousInnerClass(self, latitude, longitude, callback))
        else:
            try:
                return self._handleResponse(latitude, longitude, request.get(json.__class__), None)
            except Exception as e:
                JsonGeocoder._LOGGER.warn("Geocoder network error", e)
        return None

    class InvocationCallbackAnonymousInnerClass():


        def __init__(self, outerInstance, latitude, longitude, callback):
            self._outerInstance = outerInstance
            self._latitude = latitude
            self._longitude = longitude
            self._callback = callback

        def completed(self, json):
            super._handleResponse(self._latitude, self._longitude, json, self._callback)

        def failed(self, throwable):
            self._callback.onFailure(throwable)

    def parseAddress(self, json):
        pass

    def parseError(self, json):
        return None
