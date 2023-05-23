from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.handler.events.baseEventHandler import BaseEventHandler
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.cache.cacheManager import CacheManager




class AlertEventHandler(BaseEventHandler):


    def __init__(self, config, cacheManager):

        self._cacheManager = None
        self._ignoreDuplicateAlerts = False

        self._cacheManager = cacheManager
        self._ignoreDuplicateAlerts = config.getBoolean(Keys.EVENT_IGNORE_DUPLICATE_ALERTS)

    def analyzePosition(self, position):
        alarm = position.getAttributes().get(Position.KEY_ALARM)
        if alarm is not None:
            ignoreAlert = False
            if self._ignoreDuplicateAlerts:
                lastPosition = self._cacheManager.getPosition(position.getDeviceId())
                if lastPosition is not None and alarm is lastPosition.getAttributes().get(Position.KEY_ALARM):
                    ignoreAlert = True
            if not ignoreAlert:
                event = Event(Event.TYPE_ALARM, position)
                event.set(Position.KEY_ALARM, str(alarm))
                return "Collections.singletonMap(event, position)"
        return None
