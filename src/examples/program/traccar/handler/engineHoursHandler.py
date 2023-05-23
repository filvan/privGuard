from src.examples.program.traccar.baseDataHandler import BaseDataHandler
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.cache.cacheManager import CacheManager

class EngineHoursHandler(BaseDataHandler):

    def __init__(self, cacheManager):

        self._cacheManager = None

        self._cacheManager = cacheManager

    def handlePosition(self, position):
        if not position.hasAttribute(Position.KEY_HOURS):
            last = self._cacheManager.getPosition(position.getDeviceId())
            if last is not None:
                hours = last.getLong(Position.KEY_HOURS)
                if last.getBoolean(Position.KEY_IGNITION) and position.getBoolean(Position.KEY_IGNITION):
                    hours += position.getFixTime().getTime() - last.getFixTime().getTime()
                if hours != 0:
                    position.set(Position.KEY_HOURS, hours)
        return position
