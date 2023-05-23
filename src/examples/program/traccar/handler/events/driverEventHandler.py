import collections

from src.examples.program.traccar.handler.events.baseEventHandler import BaseEventHandler
from src.examples.program.traccar.helper.model.positionUtil import PositionUtil
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.cache.cacheManager import CacheManager

class DriverEventHandler(BaseEventHandler):


    def __init__(self, cacheManager):
        self._cacheManager = None

        self._cacheManager = cacheManager

    def analyzePosition(self, position):
        if not PositionUtil.isLatest(self._cacheManager, position):
            return None
        driverUniqueId = position.getString(Position.KEY_DRIVER_UNIQUE_ID)
        if driverUniqueId is not None:
            oldDriverUniqueId = None
            lastPosition = self._cacheManager.getPosition(position.getDeviceId())
            if lastPosition is not None:
                oldDriverUniqueId = lastPosition.getString(Position.KEY_DRIVER_UNIQUE_ID)
            if driverUniqueId != oldDriverUniqueId:
                event = Event(Event.TYPE_DRIVER_CHANGED, position)
                event.set(Position.KEY_DRIVER_UNIQUE_ID, driverUniqueId)
                return collections.singletonMap(event, position)
        return None
