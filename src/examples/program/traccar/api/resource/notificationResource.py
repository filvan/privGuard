from kafka.protocol.api import Response

from src.examples.program.traccar.api.extendedObjectResource import ExtendedObjectResource
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.notification import Notification
from src.examples.program.traccar.model.typed import Typed
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.notification.messageException import MessageException
from src.examples.program.traccar.notification.notificatorManager import NotificatorManager
from src.examples.program.traccar.storage.storageException import StorageException

class NotificationResource(ExtendedObjectResource):

    _LOGGER = "LoggerFactory.getLogger(NotificationResource.class)"


    def __init__(self):

        self._notificatorManager = None

        super().__init__(Notification.__class__)

    def get(self):
        types = list()
        fields = Event.__class__.getDeclaredFields()
        for field in fields:
            if "Modifier.isStatic(field.getModifiers())" and field.getName().startsWith("TYPE_"):
                try:
                    types.append(Typed(str(field.get(None))))
                except Exception as error:
                    NotificationResource._LOGGER.warn("Get event types error", error)
        return types

    def getNotificators(self):
        return self._notificatorManager.getAllNotificatorTypes()

    def testMessage(self):
        user = self.permissions_service.getUser(self.get_user_id())
        for method in self._notificatorManager.getAllNotificatorTypes():
            self._notificatorManager.getNotificator(method.getType()).send(None, user, Event("test", 0), None)
        return Response.noContent().build()

    def testMessage(self, notificator):
        user = self.permissions_service.getUser(self.get_user_id())
        self._notificatorManager.getNotificator(notificator).send(None, user, Event("test", 0), None)
        return Response.noContent().build()
