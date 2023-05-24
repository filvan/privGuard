from xml.dom.minidom import Entity

from src.examples.program.traccar.geolocation.geolocationException import GeolocationException
from src.examples.program.traccar.geolocation.geolocationProvider import GeolocationProvider
from src.examples.program.traccar.model.network import Network

class UniversalGeolocationProvider(GeolocationProvider):


    def __init__(self, client, url, key):

        self._client = None
        self._url = None

        self._client = client
        self._url = url + "?key=" + key

    def getLocation(self, network, callback):
        self._client.target(self._url).request().async_().post(Entity.json(network), self.InvocationCallbackAnonymousInnerClass(self, callback))

    class InvocationCallbackAnonymousInnerClass():


        def __init__(self, outerInstance, callback):
            self._outerInstance = outerInstance
            self._callback = callback

        def completed(self, json):
            if json.containsKey("error"):
                self._callback.onFailure(GeolocationException(json.getJsonObject("error").getString("message")))
            else:
                location = json.getJsonObject("location")
                self._callback.onSuccess(location.getJsonNumber("lat").doubleValue(), location.getJsonNumber("lng").doubleValue(), json.getJsonNumber("accuracy").doubleValue())

        def failed(self, throwable):
            self._callback.onFailure(throwable)
