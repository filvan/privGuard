from src.examples.program.traccar.baseDataHandler import BaseDataHandler
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.helper.model.geofenceUtil import GeofenceUtil
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.cache.cacheManager import CacheManager

class GeofenceHandler(BaseDataHandler):

    def __init__(self, config, cacheManager):

        self._config = None
        self._cacheManager = None

        self._config = config
        self._cacheManager = cacheManager

    def handlePosition(self, position):

        geofenceIds = GeofenceUtil.getCurrentGeofences(self._config, self._cacheManager, position)
        if geofenceIds:
            position.setGeofenceIds(geofenceIds)
        return position
