from src.examples.program.traccar.geocoder.address import Address
from src.examples.program.traccar.geocoder.jsonGeocoder import JsonGeocoder


class GeocodeFarmGeocoder(JsonGeocoder):

    @staticmethod
    def _formatUrl(key, language):
        url = "https://www.geocode.farm/v3/json/reverse/"
        url += "?lat=%f&lon=%f&country=us&count=1"
        if key is not None:
            url += "&key=" + key
        if language is not None:
            url += "&lang=" + language
        return url
    def __init__(self, client, key, language, cacheSize, addressFormat):
        super().__init__(client, GeocodeFarmGeocoder._formatUrl(key, language), cacheSize, addressFormat)

    def parseAddress(self, json):
        address = Address()

        result = json.getJsonObject("geocoding_results").getJsonArray("RESULTS").getJsonObject(0)

        resultAddress = result.getJsonObject("ADDRESS")

        if result.containsKey("formatted_address"):
            address.setFormattedAddress(result.getString("formatted_address"))
        if resultAddress.containsKey("street_number"):
            address.setStreet(resultAddress.getString("street_number"))
        if resultAddress.containsKey("street_name"):
            address.setStreet(resultAddress.getString("street_name"))
        if resultAddress.containsKey("locality"):
            address.setSettlement(resultAddress.getString("locality"))
        if resultAddress.containsKey("admin_1"):
            address.setState(resultAddress.getString("admin_1"))
        if resultAddress.containsKey("country"):
            address.setCountry(resultAddress.getString("country"))

        return address
