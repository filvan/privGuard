class Address:

    def __init__(self):
        self._postcode = None
        self._country = None
        self._state = None
        self._district = None
        self._settlement = None
        self._suburb = None
        self._street = None
        self._house = None
        self._formattedAddress = None



    def getPostcode(self):
        return self._postcode

    def setPostcode(self, postcode):
        self._postcode = postcode


    def getCountry(self):
        return self._country

    def setCountry(self, country):
        self._country = country


    def getState(self):
        return self._state

    def setState(self, state):
        self._state = state


    def getDistrict(self):
        return self._district

    def setDistrict(self, district):
        self._district = district


    def getSettlement(self):
        return self._settlement

    def setSettlement(self, settlement):
        self._settlement = settlement


    def getSuburb(self):
        return self._suburb

    def setSuburb(self, suburb):
        self._suburb = suburb


    def getStreet(self):
        return self._street

    def setStreet(self, street):
        self._street = street


    def getHouse(self):
        return self._house

    def setHouse(self, house):
        self._house = house


    def getFormattedAddress(self):
        return self._formattedAddress

    def setFormattedAddress(self, formattedAddress):
        self._formattedAddress = formattedAddress
