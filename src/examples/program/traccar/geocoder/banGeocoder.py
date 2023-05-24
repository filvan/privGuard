from src.examples.program.traccar.geocoder.address import Address
from src.examples.program.traccar.geocoder.jsonGeocoder import JsonGeocoder


class BanGeocoder(JsonGeocoder):

    def __init__(self, client, cacheSize, addressFormat):
        super().__init__(client, "https://api-adresse.data.gouv.fr/reverse/?lat=%f&lon=%f", cacheSize, addressFormat)

    def parseAddress(self, json):
        result = json.getJsonArray("features")

        if result is not None and not result.isEmpty():
            location = result.getJsonObject(0).getJsonObject("properties")
            address = Address()

            address.setCountry("FR")
            if location.containsKey("postcode"):
                address.setPostcode(location.getString("postcode"))
            if location.containsKey("context"):
                address.setDistrict(location.getString("context"))
            if location.containsKey("name"):
                address.setStreet(location.getString("name"))
            if location.containsKey("city"):
                address.setSettlement(location.getString("city"))
            if location.containsKey("housenumber"):
                address.setHouse(location.getString("housenumber"))
            if location.containsKey("label"):
                address.setFormattedAddress(location.getString("label"))

            return address

        return None
