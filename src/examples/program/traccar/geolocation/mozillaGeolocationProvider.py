from src.examples.program.traccar.geolocation.universalGeolocationProvider import UniversalGeolocationProvider


class MozillaGeolocationProvider(UniversalGeolocationProvider):

    _URL = "https://location.services.mozilla.com/v1/geolocate"

    def __init__(self, client, key):
        super().__init__(client, MozillaGeolocationProvider._URL,key if key is not None else "test")
