from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.model.geofence import Geofence
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.cache.cacheManager import CacheManager

class GeofenceUtil:

    def __init__(self):
        pass

    @staticmethod
    def getCurrentGeofences(config, cacheManager, position):
        result = []
        for geofence in cacheManager.getDeviceObjects(position.getDeviceId(), Geofence.__class__):
            if geofence.getGeometry().containsPoint(config, geofence, position.getLatitude(), position.getLongitude()):
                result.append(geofence.getId())
        return result
