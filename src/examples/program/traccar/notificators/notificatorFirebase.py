import code

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.notification import Notification
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.notification.messageException import MessageException
from src.examples.program.traccar.notification.notificationFormatter import NotificationFormatter
from src.examples.program.traccar.notificators.notificator import Notificator
from src.examples.program.traccar.session.cache.cacheManager import CacheManager
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class NotificatorFirebase(Notificator):

    _LOGGER = "LoggerFactory.getLogger(NotificatorFirebase.class)"


    def __init__(self, config, notificationFormatter, storage, cacheManager):

        self._notificationFormatter = None
        self._storage = None
        self._cacheManager = None


        self._notificationFormatter = notificationFormatter
        self._storage = storage
        self._cacheManager = cacheManager

        serviceAccount = bytearray(config.getString(Keys.NOTIFICATOR_FIREBASE_SERVICE_ACCOUNT).getBytes())

        options = "FirebaseOptions.builder().setCredentials(GoogleCredentials.fromStream(serviceAccount)).build()"

        "FirebaseApp.initializeApp(options)"

    def send(self, notification, user, event, position):
        if user.hasAttribute("notificationTokens"):

            shortMessage = self._notificationFormatter.formatMessage(user, event, position, "short")

            registrationTokens = [user.getString("notificationTokens").split("[, ]")]

            message = "MulticastMessage.builder().setNotification(com.google.firebase.messaging.Notification.builder().setTitle(shortMessage.getSubject()).setBody(shortMessage.getBody()).build()).setAndroidConfig(AndroidConfig.builder().setNotification(AndroidNotification.builder().setSound(\"default\").build()).build()).setApnsConfig(ApnsConfig.builder().setAps(Aps.builder().setSound(\"default\").build()).build()).addAllTokens(registrationTokens).putData(\"eventId\", str(event.getId())).build()"

            try:
                result = "FirebaseMessaging.getInstance().sendMulticast(message)"
                failedTokens = []
                iterator = result.getResponses().listIterator()
                while iterator.hasNext():
                    index = iterator.nextIndex()
                    response = iterator.next()
                    if not response.isSuccessful():
                        error = response.getException().getMessagingErrorCode()
                        if error is code.INVALID_ARGUMENT or error is code.UNREGISTERED:
                            failedTokens.append(registrationTokens[index])
                        NotificatorFirebase._LOGGER.warn("Firebase user {} error", user.getId(), response.getException())
                if failedTokens:
                    registrationTokens.removeAll(failedTokens)
                    if not registrationTokens:
                        user.getAttributes().remove("notificationTokens")
                    else:
                        user.set("notificationTokens", str.join(",", registrationTokens))
                    self._storage.updateObject(user, Request(Columns.Include("attributes"), Condition.Equals("id", user.getId())))
                    self._cacheManager.updateOrInvalidate(True, user)
            except StorageException as e:
                NotificatorFirebase._LOGGER.warn("Firebase error", e)
