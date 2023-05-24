from src.examples.program.traccar.geocoder.nominatimGeocoder import NominatimGeocoder


class LocationIqGeocoder(NominatimGeocoder):

    _DEFAULT_URL = "https://us1.locationiq.com/v1/reverse.php"

    def __init__(self, client, url, key, language, cacheSize, addressFormat):
        super().__init__(client,url if url is not None else LocationIqGeocoder._DEFAULT_URL, key, language, cacheSize, addressFormat)
