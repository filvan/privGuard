from src.examples.program.traccar.geocoder.address import Address
from src.examples.program.traccar.geocoder.jsonGeocoder import JsonGeocoder


class GeoapifyGeocoder(JsonGeocoder):

    @staticmethod
    def _formatUrl(key, language):
        url = "https://api.geoapify.com/v1/geocode/reverse?format=json&lat=%f&lon=%f"
        if key is not None:
            url += "&apiKey=" + key
        if language is not None:
            url += "&lang=" + language
        return url

    def __init__(self, client, key, language, cacheSize, addressFormat):
        super().__init__(client, GeoapifyGeocoder._formatUrl(key, language), cacheSize, addressFormat)

    def parseAddress(self, json):
        results = json.getJsonArray("results")
        if results.size() > 0:
            result = results.getJsonObject(0)

            address = Address()

            if json.containsKey("formatted"):
                address.setFormattedAddress(json.getString("formatted"))

            if result.containsKey("housenumber"):
                address.setHouse(result.getString("housenumber"))
            if result.containsKey("street"):
                address.setStreet(result.getString("street"))
            if result.containsKey("suburb"):
                address.setSuburb(result.getString("suburb"))
            if result.containsKey("city"):
                address.setSettlement(result.getString("city"))
            if result.containsKey("district"):
                address.setDistrict(result.getString("district"))
            if result.containsKey("state"):
                address.setState(result.getString("state"))
            if result.containsKey("country_code"):
                address.setCountry(result.getString("country_code").toUpperCase())
            if result.containsKey("postcode"):
                address.setPostcode(result.getString("postcode"))

            return address

        return None
