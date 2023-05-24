from src.examples.program.traccar.api.extendedObjectResource import ExtendedObjectResource
from src.examples.program.traccar.model.geofence import Geofence

class GeofenceResource(ExtendedObjectResource):

    def __init__(self):
        super().__init__(Geofence.__class__)
