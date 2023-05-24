from src.examples.program.traccar.geocoder.address import Address
from src.examples.program.traccar.geocoder.jsonGeocoder import JsonGeocoder


class MapQuestGeocoder(JsonGeocoder):

    @staticmethod
    def _formatUrl(url, key):
        if url is None:
            url = "http://www.mapquestapi.com/geocoding/v1/reverse"
        url += "?key=" + key + "&location=%f,%f"
        return url

    def __init__(self, client, url, key, cacheSize, addressFormat):
        super().__init__(client, MapQuestGeocoder._formatUrl(url, key), cacheSize, addressFormat)

    def parseAddress(self, json):
        result = json.getJsonArray("results")
        if result is not None:
            locations = result.getJsonObject(0).getJsonArray("locations")
            if locations is not None:
                location = locations.getJsonObject(0)

                address = Address()

                if location.containsKey("street"):
                    address.setStreet(location.getString("street"))
                if location.containsKey("adminArea5"):
                    address.setSettlement(location.getString("adminArea5"))
                if location.containsKey("adminArea4"):
                    address.setDistrict(location.getString("adminArea4"))
                if location.containsKey("adminArea3"):
                    address.setState(location.getString("adminArea3"))
                if location.containsKey("adminArea1"):
                    address.setCountry(location.getString("adminArea1").toUpperCase())
                if location.containsKey("postalCode"):
                    address.setPostcode(location.getString("postalCode"))

                return address
        return None
