from src.examples.program.traccar.geocoder.address import Address
from src.examples.program.traccar.geocoder.jsonGeocoder import JsonGeocoder


class OpenCageGeocoder(JsonGeocoder):

    @staticmethod
    def _formatUrl(url, key, language):
        if url is None:
            url = "https://api.opencagedata.com/geocode/v1"
        url += "/json?q=%f,%f&no_annotations=1&key=" + key
        if language is not None:
            url += "&language=" + language
        return url

    def __init__(self, client, url, key, language, cacheSize, addressFormat):
        super().__init__(client, OpenCageGeocoder._formatUrl(url, key, language), cacheSize, addressFormat)

    def parseAddress(self, json):
        result = json.getJsonArray("results")
        if result is not None:
            location = result.getJsonObject(0).getJsonObject("components")
            if location is not None:
                address = Address()

                if result.getJsonObject(0).containsKey("formatted"):
                    address.setFormattedAddress(result.getJsonObject(0).getString("formatted"))
                if location.containsKey("building"):
                    address.setHouse(location.getString("building"))
                if location.containsKey("house_number"):
                    address.setHouse(location.getString("house_number"))
                if location.containsKey("road"):
                    address.setStreet(location.getString("road"))
                if location.containsKey("suburb"):
                    address.setSuburb(location.getString("suburb"))
                if location.containsKey("city"):
                    address.setSettlement(location.getString("city"))
                if location.containsKey("city_district"):
                    address.setSettlement(location.getString("city_district"))
                if location.containsKey("county"):
                    address.setDistrict(location.getString("county"))
                if location.containsKey("state"):
                    address.setState(location.getString("state"))
                if location.containsKey("country_code"):
                    address.setCountry(location.getString("country_code").toUpperCase())
                if location.containsKey("postcode"):
                    address.setPostcode(location.getString("postcode"))

                return address
        return None
