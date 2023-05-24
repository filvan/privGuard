from src.examples.program.traccar.geocoder.address import Address
from src.examples.program.traccar.geocoder.jsonGeocoder import JsonGeocoder


class MapmyIndiaGeocoder(JsonGeocoder):

    def __init__(self, client, url, key, cacheSize, addressFormat):
        super().__init__(client, url + "/" + key + "/rev_geocode?lat=%f&lng=%f", cacheSize, addressFormat)

    def parseAddress(self, json):
        results = json.getJsonArray("results")

        if not results.isEmpty():
            address = Address()

            result = results.get(0)

            if result.containsKey("formatted_address"):
                address.setFormattedAddress(result.getString("formatted_address"))

            if result.containsKey("house_number") and not result.getString("house_number").isEmpty():
                address.setHouse(result.getString("house_number"))
            elif result.containsKey("house_name") and not result.getString("house_name").isEmpty():
                address.setHouse(result.getString("house_name"))

            if result.containsKey("street"):
                address.setStreet(result.getString("street"))

            if result.containsKey("locality") and not result.getString("locality").isEmpty():
                address.setSuburb(result.getString("locality"))
            elif result.containsKey("sublocality") and not result.getString("sublocality").isEmpty():
                address.setSuburb(result.getString("sublocality"))
            elif result.containsKey("subsublocality") and not result.getString("subsublocality").isEmpty():
                address.setSuburb(result.getString("subsublocality"))

            if result.containsKey("city") and not result.getString("city").isEmpty():
                address.setSettlement(result.getString("city"))
            elif result.containsKey("village") and not result.getString("village").isEmpty():
                address.setSettlement(result.getString("village"))

            if result.containsKey("district"):
                address.setDistrict(result.getString("district"))
            elif result.containsKey("subDistrict"):
                address.setDistrict(result.getString("subDistrict"))

            if result.containsKey("state"):
                address.setState(result.getString("state"))

            if result.containsKey("pincode"):
                address.setPostcode(result.getString("pincode"))

            return address
        return None
