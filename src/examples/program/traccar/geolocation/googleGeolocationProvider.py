from src.examples.program.traccar.geolocation.universalGeolocationProvider import UniversalGeolocationProvider


class GoogleGeolocationProvider(UniversalGeolocationProvider):

    _URL = "https://www.googleapis.com/geolocation/v1/geolocate"

    def __init__(self, client, key):
        super().__init__(client, GoogleGeolocationProvider._URL, key)
