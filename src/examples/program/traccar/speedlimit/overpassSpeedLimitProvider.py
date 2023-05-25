from src.examples.program.traccar.helper.unitsConverter import UnitsConverter
from src.examples.program.traccar.speedlimit.speedLimitException import SpeedLimitException
from src.examples.program.traccar.speedlimit.speedLimitProvider import SpeedLimitProvider


class OverpassSpeedLimitProvider(SpeedLimitProvider):


    def __init__(self, client, url):

        self._client = None
        self._url = None

        self._client = client
        self._url = url + "?data=[out:json];way[maxspeed](around:100.0,%f,%f);out%%20tags;"

    def _parseSpeed(self, value):
        if value.endswith(" mph"):
            return UnitsConverter.knotsFromMph(float(value[0:len(value) - 4]))
        elif value.endswith(" knots"):
            return float(value[0:len(value) - 6])
        elif value.matches("\\d+"):
            return UnitsConverter.knotsFromKph(float(value))
        else:
            return None

    def getSpeedLimit(self, latitude, longitude, callback):
        formattedUrl = str.format(self._url, latitude, longitude)
        invoker = self._client.target(formattedUrl).request().async_()
        invoker.get(self.InvocationCallbackAnonymousInnerClass(self, callback))

    class InvocationCallbackAnonymousInnerClass():


        def __init__(self, outerInstance, callback):
            self._outerInstance = outerInstance
            self._callback = callback

        def completed(self, json):
            elements = json.getJsonArray("elements")
            if not elements.isEmpty():
                maxSpeed = OverpassSpeedLimitProvider._parseSpeed(elements.getJsonObject(0).getJsonObject("tags").getString("maxspeed"))
                if maxSpeed is not None:
                    self._callback.onSuccess(maxSpeed)
                else:
                    self._callback.onFailure(SpeedLimitException("Parsing failed"))
            else:
                self._callback.onFailure(SpeedLimitException("Not found"))

        def failed(self, throwable):
            self._callback.onFailure(throwable)
