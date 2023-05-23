from src.examples.program.traccar.handler.events.baseEventHandler import BaseEventHandler
from src.examples.program.traccar.model.maintenance import Maintenance
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.cache.cacheManager import CacheManager

class MaintenanceEventHandler(BaseEventHandler):


    def __init__(self, cacheManager):

        self._cacheManager = None

        self._cacheManager = cacheManager

    def analyzePosition(self, position):
        lastPosition = self._cacheManager.getPosition(position.getDeviceId())
        if lastPosition is None or position.getFixTime().compareTo(lastPosition.getFixTime()) < 0:
            return None

        events = {}
        for maintenance in self._cacheManager.getDeviceObjects(position.getDeviceId(), Maintenance.__class__):
            if maintenance.getPeriod() != 0:
                oldValue = lastPosition.getDouble(maintenance.getType())
                newValue = position.getDouble(maintenance.getType())
                if oldValue != 0.0 and newValue != 0.0 and newValue >= maintenance.getStart():
                    if oldValue < maintenance.getStart() or int(((oldValue - maintenance.getStart()) / maintenance.getPeriod())) < int(((newValue - maintenance.getStart()) / maintenance.getPeriod())):
                        event = Event(Event.TYPE_MAINTENANCE, position)
                        event.setMaintenanceId(maintenance.getId())
                        event.set(maintenance.getType(), newValue)
                        events[event] = position

        return events
