from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.notification import Notification
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.notification.notificationFormatter import NotificationFormatter
from src.examples.program.traccar.notificators.notificator import Notificator
from src.examples.program.traccar.session.connectionManager import ConnectionManager

class NotificatorWeb(Notificator):
    def __init__(self, connectionManager, notificationFormatter):
        self._connectionManager = None
        self._notificationFormatter = None

        self._connectionManager = connectionManager
        self._notificationFormatter = notificationFormatter

    def send(self, notification, user, event, position):

        copy = Event()
        copy.setId(event.getId())
        copy.setDeviceId(event.getDeviceId())
        copy.setType(event.getType())
        copy.setEventTime(event.getEventTime())
        copy.setPositionId(event.getPositionId())
        copy.setGeofenceId(event.getGeofenceId())
        copy.setMaintenanceId(event.getMaintenanceId())
        copy.getAttributes().putAll(event.getAttributes())

        message = self._notificationFormatter.formatMessage(user, event, position, "short")
        copy.set("message", message.getBody())

        self._connectionManager.updateEvent(True, user.getId(), copy)
