from src.examples.program.traccar.config.config import Keys
from src.examples.program.traccar.helper.distanceCalculator import DistanceCalculator
from .geofenceGeometry import GeofenceGeometry

class GeofencePolyline(GeofenceGeometry):

    def _initialize_instance_fields(self):

        self._coordinates = None



    def __init__(self):
        self._initialize_instance_fields()


    def __init__(self, wkt):
        self._initialize_instance_fields()

        self.fromWkt(wkt)

    def containsPoint(self, config, geofence, latitude, longitude):
        distance = geofence.getDouble("polylineDistance")
        if distance == 0:
            distance = config.getDouble(Keys.GEOFENCE_POLYLINE_DISTANCE)
        for i in range(1, len(self._coordinates)):
            if DistanceCalculator.distanceToLine(latitude, longitude, self._coordinates[i - 1].getLat(), self._coordinates[i - 1].getLon(), self._coordinates[i].getLat(), self._coordinates[i].getLon()) <= distance:
                return True
        return False

    def calculateArea(self):
        return 0

    def toWkt(self):
        buf = ""
        buf += ("LINESTRING (")
        for coordinate in self._coordinates:
            buf += (coordinate.getLat())
            buf += (" ")
            buf += (coordinate.getLon())
            buf += (", ")
        return buf.substring(0, buf.length() - 2) + ")"

    def fromWkt(self, wkt):
        if self._coordinates is None:
            self._coordinates = []
        else:
            self._coordinates.clear()

        if not wkt.startswith("LINESTRING"):
            raise Exception("Mismatch geometry type", 0)
        content = wkt[wkt.find("(") + 1:wkt.find(")")]
        if not content:
            raise Exception("No content", 0)
        commaTokens = content.split(",")
        if len(commaTokens) < 2:
            raise Exception("Not valid content", 0)

        for commaToken in commaTokens:
            tokens = commaToken.trim().split("\\s")
            if len(tokens) != 2:
                raise Exception("Here must be two coordinates: " + commaToken, 0)
            coordinate = self.Coordinate()
            try:
                coordinate.setLat(float(tokens[0]))
            except Exception as e:
                raise Exception(tokens[0] + " is not a double", 0)
            try:
                coordinate.setLon(float(tokens[1]))
            except Exception as e:
                raise Exception(tokens[1] + " is not a double", 0)
            self._coordinates += (coordinate)
