from src.examples.program.traccar.handler.events.baseEventHandler import BaseEventHandler
from src.examples.program.traccar.helper.model.positionUtil import PositionUtil
from src.examples.program.traccar.model.calendar import Calendar
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.geofence import Geofence
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.cache.cacheManager import CacheManager

class GeofenceEventHandler(BaseEventHandler):


    def __init__(self, cacheManager):

        self._cacheManager = None

        self._cacheManager = cacheManager

    def analyzePosition(self, position):
        if not PositionUtil.isLatest(self._cacheManager, position):
            return None

        oldGeofences = []
        lastPosition = self._cacheManager.getPosition(position.getDeviceId())
        if lastPosition is not None and lastPosition.getGeofenceIds() is not None:
            oldGeofences.extend(lastPosition.getGeofenceIds())

        newGeofences = []
        if position.getGeofenceIds() is not None:
            newGeofences.extend(position.getGeofenceIds())
            newGeofences.removeAll(oldGeofences)
            oldGeofences.removeAll(position.getGeofenceIds())

        events = {}
        for geofenceId in oldGeofences:
            geofence = self._cacheManager.getObject(Geofence.__class__, geofenceId)
            if geofence is not None:
                calendarId = geofence.getCalendarId()
                calendar = self._cacheManager.getObject(Calendar.__class__, calendarId) if calendarId != 0 else None
                if calendar is None or calendar.checkMoment(position.getFixTime()):
                    event = Event(Event.TYPE_GEOFENCE_EXIT, position)
                    event.setGeofenceId(geofenceId)
                    events[event] = position
        for geofenceId in newGeofences:
            calendarId = self._cacheManager.getObject(Geofence.__class__, geofenceId).getCalendarId()
            calendar = self._cacheManager.getObject(Calendar.__class__, calendarId) if calendarId != 0 else None
            if calendar is None or calendar.checkMoment(position.getFixTime()):
                event = Event(Event.TYPE_GEOFENCE_ENTER, position)
                event.setGeofenceId(geofenceId)
                events[event] = position
        return events
