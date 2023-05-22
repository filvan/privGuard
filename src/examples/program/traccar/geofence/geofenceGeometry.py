class GeofenceGeometry:

    def containsPoint(self, config, geofence, latitude, longitude):
        pass

    def calculateArea(self):
        pass

    def toWkt(self):
        pass

    def fromWkt(self, wkt):
        pass

    class Coordinate:

        def __init__(self):

            self._lat = 0
            self._lon = 0



        def getLat(self):
            return self._lat

        def setLat(self, lat):
            self._lat = lat

        def getLon(self):
            return self._lon

        def setLon(self, lon):
            self._lon = lon
