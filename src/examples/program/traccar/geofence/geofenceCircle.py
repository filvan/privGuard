from .geofenceGeometry import GeofenceGeometry
from src.examples.program.traccar.helper.distanceCalculator import DistanceCalculator

import math

class GeofenceCircle(GeofenceGeometry):

    def _initialize_instance_fields(self):

        self._centerLatitude = 0
        self._centerLongitude = 0
        self._radius = 0





    def __init__(self):
        self._initialize_instance_fields()





    def __init__(self, wkt):
        self._initialize_instance_fields()

        self.fromWkt(wkt)



    def __init__(self, latitude, longitude, radius):
        self._initialize_instance_fields()

        self._centerLatitude = latitude
        self._centerLongitude = longitude
        self._radius = radius

    def distanceFromCenter(self, latitude, longitude):
        return DistanceCalculator.distance(self._centerLatitude, self._centerLongitude, latitude, longitude)

    def containsPoint(self, config, geofence, latitude, longitude):
        return self.distanceFromCenter(latitude, longitude) <= self._radius

    def calculateArea(self):
        return math.pi * self._radius * self._radius

    def toWkt(self):
        wkt = None
        wkt = "CIRCLE ("
        wkt += str(self._centerLatitude)
        wkt += " "
        wkt += str(self._centerLongitude)
        wkt += ", "
        format = "0.#"
        wkt += format.format(self._radius)
        wkt += ")"
        return wkt



    def fromWkt(self, wkt):
        if not wkt.startswith("CIRCLE"):
            raise Exception("Mismatch geometry type", 0)
        content = wkt[wkt.find("(") + 1:wkt.find(")")]
        if content == "":
            raise Exception("No content", 0)
        commaTokens = content.split(",")
        if len(commaTokens) != 2:
            raise Exception("Not valid content", 0)
        tokens = commaTokens[0].split("\\s")
        if len(tokens) != 2:
            raise Exception("Too much or less coordinates", 0)
        try:
            self._centerLatitude = float(tokens[0])
        except Exception as e:
            raise Exception(tokens[0] + " is not a double", 0)
        try:
            self._centerLongitude = float(tokens[1])
        except Exception as e:
            raise Exception(tokens[1] + " is not a double", 0)
        try:
            self._radius = float(commaTokens[1])
        except Exception as e:
            raise Exception(commaTokens[1] + " is not a double", 0)
