from src.examples.program.traccar.geocoder.address import Address
from src.examples.program.traccar.geocoder.jsonGeocoder import JsonGeocoder


class GeocodeXyzGeocoder(JsonGeocoder):

    @staticmethod
    def _formatUrl(key):
        url = "https://geocode.xyz/%f,%f?geoit=JSON"
        if key is not None:
            url += "&key=" + key
        return url

    def __init__(self, client, key, cacheSize, addressFormat):
        super().__init__(client, GeocodeXyzGeocoder._formatUrl(key), cacheSize, addressFormat)

    def parseAddress(self, json):
        address = Address()

        if json.containsKey("stnumber"):
            address.setHouse(json.getString("stnumber"))
        if json.containsKey("staddress"):
            address.setStreet(json.getString("staddress"))
        if json.containsKey("city"):
            address.setSettlement(json.getString("city"))
        if json.containsKey("region"):
            address.setState(json.getString("region"))
        if json.containsKey("prov"):
            address.setCountry(json.getString("prov"))
        if json.containsKey("postal"):
            address.setPostcode(json.getString("postal"))

        return address
