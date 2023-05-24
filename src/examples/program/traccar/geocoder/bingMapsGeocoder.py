from src.examples.program.traccar.geocoder.address import Address
from src.examples.program.traccar.geocoder.jsonGeocoder import JsonGeocoder


class BingMapsGeocoder(JsonGeocoder):

    def __init__(self, client, url, key, cacheSize, addressFormat):
        super().__init__(client, url + "/Locations/%f,%f?key=" + key + "&include=ciso2", cacheSize, addressFormat)

    def parseAddress(self, json):
        result = json.getJsonArray("resourceSets")
        if result is not None:
            location = result.getJsonObject(0).getJsonArray("resources").getJsonObject(0).getJsonObject("address")
            if location is not None:
                address = Address()
                if location.containsKey("addressLine"):
                    address.setStreet(location.getString("addressLine"))
                if location.containsKey("locality"):
                    address.setSettlement(location.getString("locality"))
                if location.containsKey("adminDistrict2"):
                    address.setDistrict(location.getString("adminDistrict2"))
                if location.containsKey("adminDistrict"):
                    address.setState(location.getString("adminDistrict"))
                if location.containsKey("countryRegionIso2"):
                    address.setCountry(location.getString("countryRegionIso2").toUpperCase())
                if location.containsKey("postalCode"):
                    address.setPostcode(location.getString("postalCode"))
                if location.containsKey("formattedAddress"):
                    address.setFormattedAddress(location.getString("formattedAddress"))
                return address
        return None
