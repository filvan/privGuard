from src.examples.program.traccar.geocoder.address import Address
from src.examples.program.traccar.geocoder.jsonGeocoder import JsonGeocoder


class GoogleGeocoder(JsonGeocoder):

    @staticmethod
    def _formatUrl(key, language):
        url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=%f,%f"
        if key is not None:
            url += "&key=" + key
        if language is not None:
            url += "&language=" + language
        return url

    def __init__(self, client, key, language, cacheSize, addressFormat):
        super().__init__(client, GoogleGeocoder._formatUrl(key, language), cacheSize, addressFormat)

    def parseAddress(self, json):
        results = json.getJsonArray("results")

        if not results.isEmpty():
            address = Address()

            result = results.get(0)
            components = result.getJsonArray("address_components")

            if result.containsKey("formatted_address"):
                address.setFormattedAddress(result.getString("formatted_address"))

            for component in components.getValuesAs(json.__class__):

                value = component.getString("short_name")

                for type in component.getJsonArray("types").getValuesAs(str.__class__):

                    if type.getString() is "street_number":
                        address.setHouse(value)
                    if (type.getString() is "street_number") or (type.getString() is "route"):
                        address.setStreet(value)
                    if (type.getString() is "street_number") or (type.getString() is "route") or (type.getString() is "locality"):
                        address.setSettlement(value)
                    if (type.getString() is "street_number") or (type.getString() is "route") or (type.getString() is "locality") or (type.getString() is "administrative_area_level_2"):
                        address.setDistrict(value)
                    if (type.getString() is "street_number") or (type.getString() is "route") or (type.getString() is "locality") or (type.getString() is "administrative_area_level_2") or (type.getString() is "administrative_area_level_1"):
                        address.setState(value)
                    if (type.getString() is "street_number") or (type.getString() is "route") or (type.getString() is "locality") or (type.getString() is "administrative_area_level_2") or (type.getString() is "administrative_area_level_1") or (type.getString() is "country"):
                        address.setCountry(value)
                    if (type.getString() is "street_number") or (type.getString() is "route") or (type.getString() is "locality") or (type.getString() is "administrative_area_level_2") or (type.getString() is "administrative_area_level_1") or (type.getString() is "country") or (type.getString() is "postal_code"):
                        address.setPostcode(value)

            return address

        return None

    def parseError(self, json):
        return json.getString("error_message")
