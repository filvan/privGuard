from src.examples.program.traccar.geocoder.address import Address
from src.examples.program.traccar.geocoder.jsonGeocoder import JsonGeocoder


class TomTomGeocoder(JsonGeocoder):

    @staticmethod
    def _formatUrl(url, key):
        if url is None:
            url = "https://api.tomtom.com/search/2/reverseGeocode/"
        url += "%f,%f.json?key=" + key
        return url

    def __init__(self, client, url, key, cacheSize, addressFormat):
        super().__init__(client, TomTomGeocoder._formatUrl(url, key), cacheSize, addressFormat)

    def parseAddress(self, json):
        addresses = json.getJsonArray("addresses")
        if addresses is not None:
            record = addresses.getJsonObject(0)
            if record is not None:
                location = record.getJsonObject("address")

                address = Address()

                if location.containsKey("streetNumber"):
                    address.setHouse(location.getString("streetNumber"))
                if location.containsKey("street"):
                    address.setStreet(location.getString("street"))
                if location.containsKey("municipality"):
                    address.setSettlement(location.getString("municipality"))
                if location.containsKey("municipalitySubdivision"):
                    address.setDistrict(location.getString("municipalitySubdivision"))
                if location.containsKey("countrySubdivision"):
                    address.setState(location.getString("countrySubdivision"))
                if location.containsKey("country"):
                    address.setCountry(location.getString("country").toUpperCase())
                if location.containsKey("postalCode"):
                    address.setPostcode(location.getString("postalCode"))

                return address
        return None
