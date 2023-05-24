from src.examples.program.traccar.geocoder.address import Address
from src.examples.program.traccar.geocoder.jsonGeocoder import JsonGeocoder


class NominatimGeocoder(JsonGeocoder):

    @staticmethod
    def _formatUrl(url, key, language):
        if url is None:
            url = "https://nominatim.openstreetmap.org/reverse"
        url += "?format=json&lat=%f&lon=%f&zoom=18&addressdetails=1"
        if key is not None:
            url += "&key=" + key
        if language is not None:
            url += "&accept-language=" + language
        return url

    def __init__(self, client, url, key, language, cacheSize, addressFormat):
        super().__init__(client, NominatimGeocoder._formatUrl(url, key, language), cacheSize, addressFormat)

    def parseAddress(self, json):
        result = json.getJsonObject("address")

        if result is not None:
            address = Address()

            if json.containsKey("display_name"):
                address.setFormattedAddress(json.getString("display_name"))

            if result.containsKey("house_number"):
                address.setHouse(result.getString("house_number"))
            if result.containsKey("road"):
                address.setStreet(result.getString("road"))
            if result.containsKey("suburb"):
                address.setSuburb(result.getString("suburb"))

            if result.containsKey("village"):
                address.setSettlement(result.getString("village"))
            elif result.containsKey("town"):
                address.setSettlement(result.getString("town"))
            elif result.containsKey("city"):
                address.setSettlement(result.getString("city"))

            if result.containsKey("state_district"):
                address.setDistrict(result.getString("state_district"))
            elif result.containsKey("region"):
                address.setDistrict(result.getString("region"))

            if result.containsKey("state"):
                address.setState(result.getString("state"))
            if result.containsKey("country_code"):
                address.setCountry(result.getString("country_code").toUpperCase())
            if result.containsKey("postcode"):
                address.setPostcode(result.getString("postcode"))

            return address

        return None
