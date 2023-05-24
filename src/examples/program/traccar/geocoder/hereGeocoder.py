from src.examples.program.traccar.geocoder.address import Address
from src.examples.program.traccar.geocoder.jsonGeocoder import JsonGeocoder


class HereGeocoder(JsonGeocoder):

    @staticmethod
    def _formatUrl(url, id, key, language):
        if url is None:
            url = "https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json"
        url += "?mode=retrieveAddresses&maxresults=1"
        url += "&prox=%f,%f,0"
        url += "&app_id=" + id
        url += "&app_code=" + key
        url += "&apiKey=" + key
        if language is not None:
            url += "&language=" + language
        return url

    def __init__(self, client, url, id, key, language, cacheSize, addressFormat):
        super().__init__(client, HereGeocoder._formatUrl(url, id, key, language), cacheSize, addressFormat)

    def parseAddress(self, json):
        result = json.getJsonObject("Response").getJsonArray("View").getJsonObject(0).getJsonArray("Result").getJsonObject(0).getJsonObject("Location").getJsonObject("Address")

        if result is not None:
            address = Address()

            if result.containsKey("Label"):
                address.setFormattedAddress(result.getString("Label"))

            if result.containsKey("HouseNumber"):
                address.setHouse(result.getString("HouseNumber"))
            if result.containsKey("Street"):
                address.setStreet(result.getString("Street"))
            if result.containsKey("City"):
                address.setSettlement(result.getString("City"))
            if result.containsKey("District"):
                address.setDistrict(result.getString("District"))
            if result.containsKey("State"):
                address.setState(result.getString("State"))
            if result.containsKey("Country"):
                address.setCountry(result.getString("Country").toUpperCase())
            if result.containsKey("PostalCode"):
                address.setPostcode(result.getString("PostalCode"))

            return address

        return None
