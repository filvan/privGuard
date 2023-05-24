from src.examples.program.traccar.geocoder.address import Address
from src.examples.program.traccar.geocoder.jsonGeocoder import JsonGeocoder


class PositionStackGeocoder(JsonGeocoder):

    @staticmethod
    def _formatUrl(key):
        return "http://api.positionstack.com/v1/reverse?access_key=" + key + "&query=%f,%f"

    def __init__(self, client, key, cacheSize, addressFormat):
        super().__init__(client, PositionStackGeocoder._formatUrl(key), cacheSize, addressFormat)

    def parseAddress(self, json):
        result = json.getJsonArray("data")

        if result is not None and not result.isEmpty():
            record = result.getJsonObject(0)

            address = Address()

            address.setFormattedAddress(self.readValue(record, "label"))
            address.setHouse(self.readValue(record, "number"))
            address.setStreet(self.readValue(record, "street"))
            address.setSuburb(self.readValue(record, "neighbourhood"))
            address.setSettlement(self.readValue(record, "locality"))
            address.setState(self.readValue(record, "region"))
            address.setCountry(self.readValue(record, "country_code"))
            address.setPostcode(self.readValue(record, "postal_code"))

            return address

        return None
