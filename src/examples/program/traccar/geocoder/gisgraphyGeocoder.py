from src.examples.program.traccar.geocoder.address import Address
from src.examples.program.traccar.geocoder.jsonGeocoder import JsonGeocoder


class GisgraphyGeocoder(JsonGeocoder):

    @staticmethod
    def _formatUrl(url):
        if url is None:
            url = "http://services.gisgraphy.com/reversegeocoding/search"
        url += "?format=json&lat=%f&lng=%f&from=1&to=1"
        return url

    def __init__(self, client, url, cacheSize, addressFormat):
        super().__init__(client, GisgraphyGeocoder._formatUrl(url), cacheSize, addressFormat)

    def parseAddress(self, json):
        address = Address()

        result = json.getJsonArray("result").getJsonObject(0)

        if result.containsKey("streetName"):
            address.setStreet(result.getString("streetName"))
        if result.containsKey("city"):
            address.setSettlement(result.getString("city"))
        if result.containsKey("state"):
            address.setState(result.getString("state"))
        if result.containsKey("countryCode"):
            address.setCountry(result.getString("countryCode"))
        if result.containsKey("formatedFull"):
            address.setFormattedAddress(result.getString("formatedFull"))

        return address
