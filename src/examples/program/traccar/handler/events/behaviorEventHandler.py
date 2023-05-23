import collections

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.handler.events.baseEventHandler import BaseEventHandler
from src.examples.program.traccar.helper.unitsConverter import UnitsConverter
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.cache.cacheManager import CacheManager

class BehaviorEventHandler(BaseEventHandler):



    def __init__(self, config, cacheManager):

        self._accelerationThreshold = 0
        self._brakingThreshold = 0
        self._cacheManager = None

        self._accelerationThreshold = config.getDouble(Keys.EVENT_BEHAVIOR_ACCELERATION_THRESHOLD)
        self._brakingThreshold = config.getDouble(Keys.EVENT_BEHAVIOR_BRAKING_THRESHOLD)
        self._cacheManager = cacheManager

    def analyzePosition(self, position):

        lastPosition = self._cacheManager.getPosition(position.getDeviceId())
        if lastPosition is not None and position.getFixTime() is lastPosition.getFixTime():
            acceleration = UnitsConverter.mpsFromKnots(position.getSpeed() - lastPosition.getSpeed()) * 1000 / (position.getFixTime().getTime() - lastPosition.getFixTime().getTime())
            if self._accelerationThreshold != 0 and acceleration >= self._accelerationThreshold:
                event = Event(Event.TYPE_ALARM, position)
                event.set(Position.KEY_ALARM, Position.ALARM_ACCELERATION)
                return collections.singletonMap(event, position)
            elif self._brakingThreshold != 0 and acceleration <= -self._brakingThreshold:
                event = Event(Event.TYPE_ALARM, position)
                event.set(Position.KEY_ALARM, Position.ALARM_BRAKING)
                return collections.singletonMap(event, position)
        return None
