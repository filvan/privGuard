from src.examples.program.traccar.geocoder.address import Address
from src.examples.program.traccar.geocoder.jsonGeocoder import JsonGeocoder


class MapboxGeocoder(JsonGeocoder):

    @staticmethod
    def _formatUrl(key):
        return "https://api.mapbox.com/geocoding/v5/mapbox.places/%2$f,%1$f.json?access_token=" + key

    def __init__(self, client, key, cacheSize, addressFormat):
        super().__init__(client, MapboxGeocoder._formatUrl(key), cacheSize, addressFormat)

    def parseAddress(self, json):
        features = json.getJsonArray("features")

        if not features.isEmpty():
            address = Address()

            mostSpecificFeature = features.get(0)

            if mostSpecificFeature.containsKey("place_name"):
                address.setFormattedAddress(mostSpecificFeature.getString("place_name"))

            if mostSpecificFeature.containsKey("address"):
                address.setHouse(mostSpecificFeature.getString("address"))

            for feature in features.getValuesAs(json.__class__):

                value = feature.getString("text")

                for type in feature.getJsonArray("place_type").getValuesAs(str.__class__):

                    if type.getString() is "address":
                        address.setStreet(value)
                    if (type.getString() is "address") or (type.getString() is "neighborhood"):
                        address.setSuburb(value)
                    if (type.getString() is "address") or (type.getString() is "neighborhood") or (type.getString() is "postcode"):
                        address.setPostcode(value)
                    if (type.getString() is "address") or (type.getString() is "neighborhood") or (type.getString() is "postcode") or (type.getString() is "locality"):
                        address.setSettlement(value)
                    if (type.getString() is "address") or (type.getString() is "neighborhood") or (type.getString() is "postcode") or (type.getString() is "locality") or (type.getString() is "district") or (type.getString() is "place"):
                        address.setDistrict(value)
                    if (type.getString() is "address") or (type.getString() is "neighborhood") or (type.getString() is "postcode") or (type.getString() is "locality") or (type.getString() is "district") or (type.getString() is "place") or (type.getString() is "region"):
                        address.setState(value)
                    if (type.getString() is "address") or (type.getString() is "neighborhood") or (type.getString() is "postcode") or (type.getString() is "locality") or (type.getString() is "district") or (type.getString() is "place") or (type.getString() is "region") or (type.getString() is "country"):
                        address.setCountry(value)

            return address
        return None
