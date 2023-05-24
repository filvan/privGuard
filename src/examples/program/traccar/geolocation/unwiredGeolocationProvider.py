from xml.dom.minidom import Entity

from src.examples.program.traccar.geolocation.geolocationException import GeolocationException
from src.examples.program.traccar.geolocation.geolocationProvider import GeolocationProvider
from src.examples.program.traccar.model.cellTower import CellTower
from src.examples.program.traccar.model.network import Network
from src.examples.program.traccar.model.wifiAccessPoint import WifiAccessPoint

class UnwiredGeolocationProvider(GeolocationProvider):



    class NetworkMixIn:
        def getHomeMobileCountryCode(self):
            pass
        def getHomeMobileNetworkCode(self):
            pass
        def getRadioType(self):
            pass
        def getCarrier(self):
            pass
        def getConsiderIp(self):
            pass
        def getCellTowers(self):
            pass
        def getWifiAccessPoints(self):
            pass

    class CellTowerMixIn:
        def getRadioType(self):
            pass
        def getMobileCountryCode(self):
            pass
        def getMobileNetworkCode(self):
            pass
        def getLocationAreaCode(self):
            pass
        def getCellId(self):
            pass

    class WifiAccessPointMixIn:
        def getMacAddress(self):
            pass
        def getSignalStrength(self):
            pass

    def __init__(self, client, url, key):

        self._client = None
        self._url = None
        self._key = None
        self._objectMapper = None

        self._client = client
        self._url = url
        self._key = key

        self._objectMapper = "ObjectMapper()"
        self._objectMapper.addMixIn(Network.__class__, self.NetworkMixIn.__class__)
        self._objectMapper.addMixIn(CellTower.__class__, self.CellTowerMixIn.__class__)
        self._objectMapper.addMixIn(WifiAccessPoint.__class__, self.WifiAccessPointMixIn.__class__)

    def getLocation(self, network, callback):
        json = self._objectMapper.valueToTree(network)
        json.put("token", self._key)

        self._client.target(self._url).request().async_().post(Entity.json(json), self.InvocationCallbackAnonymousInnerClass(self, callback))

    class InvocationCallbackAnonymousInnerClass():


        def __init__(self, outerInstance, callback):
            self._outerInstance = outerInstance
            self._callback = callback

        def completed(self, json):
            if json.getString("status") is "error":
                self._callback.onFailure(GeolocationException(json.getString("message")))
            else:
                self._callback.onSuccess(json.getJsonNumber("lat").doubleValue(), json.getJsonNumber("lon").doubleValue(), json.getJsonNumber("accuracy").doubleValue())

        def failed(self, throwable):
            self._callback.onFailure(throwable)
