from src.examples.program.traccar.geocoder.address import Address
from src.examples.program.traccar.geocoder.jsonGeocoder import JsonGeocoder


class MapTilerGeocoder(JsonGeocoder):

    def __init__(self, client, key, cacheSize, addressFormat):
        super().__init__(client, "https://api.maptiler.com/geocoding/%2$f,%1$f.json?key=" + key, cacheSize, addressFormat)

    def parseAddress(self, json):
        features = json.getJsonArray("features")

        if not features.isEmpty():
            address = Address()

            for i, unusedItem in enumerate(features):
                feature = features.getJsonObject(i)
                type = feature.getJsonArray("place_type").getString(0)
                value = feature.getString("text")
                if type == "street":
                    address.setStreet(value)
                elif type == "city":
                    address.setSettlement(value)
                elif type == "county":
                    address.setDistrict(value)
                elif type == "state":
                    address.setState(value)
                elif type == "country":
                    address.setCountry(value)
                if address.getFormattedAddress() is None:
                    address.setFormattedAddress(feature.getString("place_name"))

            return address

        return None

    def parseError(self, json):
        return None
