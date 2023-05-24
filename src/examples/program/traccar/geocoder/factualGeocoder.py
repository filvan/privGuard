from src.examples.program.traccar.geocoder.address import Address
from src.examples.program.traccar.geocoder.jsonGeocoder import JsonGeocoder


class FactualGeocoder(JsonGeocoder):

    @staticmethod
    def _formatUrl(url, key):
        if url is None:
            url = "https://api.factual.com/geotag"
        url += "?latitude=%f&longitude=%f&KEY=" + key
        return url

    def __init__(self, client, url, key, cacheSize, addressFormat):
        super().__init__(client, FactualGeocoder._formatUrl(url, key), cacheSize, addressFormat)

    def parseAddress(self, json):
        result = json.getJsonObject("response").getJsonObject("data")
        if result is not None:
            address = Address()
            if result.getJsonObject("street_number") is not None:
                address.setHouse(result.getJsonObject("street_number").getString("name"))
            if result.getJsonObject("street_name") is not None:
                address.setStreet(result.getJsonObject("street_name").getString("name"))
            if result.getJsonObject("locality") is not None:
                address.setSettlement(result.getJsonObject("locality").getString("name"))
            if result.getJsonObject("county") is not None:
                address.setDistrict(result.getJsonObject("county").getString("name"))
            if result.getJsonObject("region") is not None:
                address.setState(result.getJsonObject("region").getString("name"))
            if result.getJsonObject("country") is not None:
                address.setCountry(result.getJsonObject("country").getString("name"))
            if result.getJsonObject("postcode") is not None:
                address.setPostcode(result.getJsonObject("postcode").getString("name"))
            return address
        return None
