from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.forward.eventData import EventData
from src.examples.program.traccar.forward.eventForwarder import EventForwarder
from src.examples.program.traccar.geocoder.geocoder import Geocoder
from src.examples.program.traccar.model.calendar import Calendar
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.geofence import Geofence
from src.examples.program.traccar.model.maintenance import Maintenance
from src.examples.program.traccar.model.notification import Notification
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.notification.messageException import MessageException
from src.examples.program.traccar.notification.notificatorManager import NotificatorManager
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.request import Request

class NotificationManager:

    _LOGGER = "LoggerFactory.getLogger(NotificationManager.__class__)"



    def __init__(self, config, storage, cacheManager, eventForwarder, notificatorManager, geocoder):
        self._storage = None
        self._cacheManager = None
        self._eventForwarder = None
        self._notificatorManager = None
        self._geocoder = None
        self._geocodeOnRequest = False

        self._storage = storage
        self._cacheManager = cacheManager
        self._eventForwarder = eventForwarder
        self._notificatorManager = notificatorManager
        self._geocoder = geocoder
        self._geocodeOnRequest = config.getBoolean(Keys.GEOCODER_ON_REQUEST)

    def _updateEvent(self, event, position):
        try:
            event.setId(self._storage.addObject(event, Request(Columns.Exclude("id"))))
        except StorageException as error:
            NotificationManager._LOGGER.warn("Event save error", error)

        #        var notifications = cacheManager.getDeviceObjects(event.getDeviceId(), Notification.__class__).stream().filter(notification -> notification.getType().equals(event.getType())).filter(notification ->
        #        {
        #                    if (event.getType().equals(Event.TYPE_ALARM))
        #                    {
        #                        String alarmsAttribute = notification.getString("alarms")
        #                        if (alarmsAttribute != null)
        #                        {
        #                            return Arrays.asList(alarmsAttribute.split(",")).contains(event.getString(Position.KEY_ALARM))
        #                        }
        #                        return false
        #                    }
        #                    return true
        #                }
        #                ).filter(notification ->
        #                {
        #                    long calendarId = notification.getCalendarId()
        #                    Calendar calendar = calendarId != 0 ? cacheManager.getObject(Calendar.__class__, calendarId) : null
        #                    return calendar == null || calendar.checkMoment(event.getEventTime())
        #                }
        #                ).collect(Collectors.toUnmodifiableList())

        if not self.notifications.isEmpty():
            if position is not None and position.getAddress() is None and self._geocodeOnRequest and self._geocoder is not None:
                position.setAddress(self._geocoder.getAddress(position.getLatitude(), position.getLongitude(), None))

            #            notifications.forEach(notification ->
            #            {
            #                cacheManager.getNotificationUsers(notification.getId(), event.getDeviceId()).forEach(user ->
            #                {
            #                    for (String notificator : notification.getNotificatorsTypes())
            #                    {
            #                        try
            #                        {
            #                            notificatorManager.getNotificator(notificator).send(notification, user, event, position)
            #                        }
            #                        catch (MessageException exception)
            #                        {
            #                            LOGGER.warn("Notification failed", exception)
            #                        }
            #                    }
            #                }
            #                )
            #            }
            #            )

        self._forwardEvent(event, position)

    def _forwardEvent(self, event, position):
        if self._eventForwarder is not None:
            eventData = EventData()
            eventData.setEvent(event)
            eventData.setPosition(position)
            eventData.setDevice(self._cacheManager.getObject(Device.__class__, event.getDeviceId()))
            if event.getGeofenceId() != 0:
                eventData.setGeofence(self._cacheManager.getObject(Geofence.__class__, event.getGeofenceId()))
            if event.getMaintenanceId() != 0:
                eventData.setMaintenance(self._cacheManager.getObject(Maintenance.__class__, event.getMaintenanceId()))
            #JAVA TO PYTHON CONVERTER TASK: Only expression lambdas are converted by Java to Python Converter:
            #            eventForwarder.forward(eventData, (success, throwable) ->
            #            {
            #                if (!success)
            #                {
            #                    LOGGER.warn("Event forwarding failed", throwable)
            #                }
            #            }
            #            )

    def updateEvents(self, events):
        for entry in events.entrySet():
            event = entry.getKey()
            position = entry.getValue()
            try:
                self._cacheManager.addDevice(event.getDeviceId())
                self._updateEvent(event, position)
            except StorageException as e:
                raise Exception(e)
            finally:
                self._cacheManager.removeDevice(event.getDeviceId())

