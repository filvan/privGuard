from src.examples.program.traccar.geolocation.geolocationException import GeolocationException
from src.examples.program.traccar.geolocation.geolocationProvider import GeolocationProvider
from src.examples.program.traccar.model.cellTower import CellTower
from src.examples.program.traccar.model.network import Network

class OpenCellIdGeolocationProvider(GeolocationProvider):


    def __init__(self, client, url, key):

        self._client = None
        self._url = None

        self._client = client
        if url is None:
            url = "http://opencellid.org/cell/get"
        self._url = url + "?format=json&mcc=%d&mnc=%d&lac=%d&cellid=%d&key=" + key

    def getLocation(self, network, callback):
        if network.getCellTowers() is not None and not network.getCellTowers().isEmpty():

            cellTower = network.getCellTowers().iterator().next()
            request = str.format(self._url, cellTower.getMobileCountryCode(), cellTower.getMobileNetworkCode(), cellTower.getLocationAreaCode(), cellTower.getCellId())

            self._client.target(request).request().async_().get(self.InvocationCallbackAnonymousInnerClass(self, callback))

        else:
            callback.onFailure(GeolocationException("No network information"))

    class InvocationCallbackAnonymousInnerClass():


        def __init__(self, outerInstance, callback):
            self._outerInstance = outerInstance
            self._callback = callback

        def completed(self, json):
            if json.containsKey("lat") and json.containsKey("lon"):
                self._callback.onSuccess(json.getJsonNumber("lat").doubleValue(), json.getJsonNumber("lon").doubleValue(), 0)
            else:
                if json.containsKey("error"):
                    errorMessage = json.getString("error")
                    if json.containsKey("code"):
                        errorMessage += " (" + json.getInt("code") + ")"
                    self._callback.onFailure(GeolocationException(errorMessage))
                else:
                    self._callback.onFailure(GeolocationException("Coordinates are missing"))

        def failed(self, throwable):
            self._callback.onFailure(throwable)
