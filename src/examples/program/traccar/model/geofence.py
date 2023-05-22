from src.examples.program.traccar.geofence.geofenceGeometry import GeofenceGeometry
from src.examples.program.traccar.geofence.geofencePolyline import GeofencePolyline
from src.examples.program.traccar.geofence.geofencePolygon import GeofencePolygon
from src.examples.program.traccar.geofence.geofenceCircle import GeofenceCircle
from .scheduledModel import ScheduledModel
from src.examples.program.traccar.storage.queryIgnore import QueryIgnore
from src.examples.program.traccar.storage.storageName import StorageName

class Geofence(ScheduledModel):

    def __init__(self):

        self._name = None
        self._description = None
        self._area = None
        self._geometry = None



    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name


    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description


    def getArea(self):
        return self._area

    def setArea(self, area):

        if area.startswith("CIRCLE"):
            self._geometry = GeofenceCircle(area)
        elif area.startswith("POLYGON"):
            self._geometry = GeofencePolygon(area)
        elif area.startswith("LINESTRING"):
            self._geometry = GeofencePolyline(area)
        else:
            raise Exception("Unknown geometry type", 0)

        self._area = area


    def getGeometry(self):
        return self._geometry

    def setGeometry(self, geometry):
        self._area = geometry.toWkt()
        self._geometry = geometry
