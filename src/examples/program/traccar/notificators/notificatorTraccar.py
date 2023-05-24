from xml.dom.minidom import Entity

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.notification.notificationFormatter import NotificationFormatter
from src.examples.program.traccar.notificators.notificator import Notificator
from src.examples.program.traccar.session.cache.cacheManager import CacheManager
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request


class NotificatorTraccar(Notificator):

    _LOGGER = "LoggerFactory.getLogger(NotificatorTraccar.class)"



    class NotificationObject:

        def __init__(self):

            self._title = None
            self._body = None
            self._sound = None


    class Message:

        def __init__(self):

            self._tokens = None
            self._notification = None


    def __init__(self, config, notificationFormatter, client, storage, cacheManager):

        self._notificationFormatter = None
        self._client = None
        self._storage = None
        self._cacheManager = None
        self._url = None
        self._key = None

        self._notificationFormatter = notificationFormatter
        self._client = client
        self._storage = storage
        self._cacheManager = cacheManager
        self._url = "https://www.traccar.org/push/"
        self._key = config.getString(Keys.NOTIFICATOR_TRACCAR_KEY)

    def send(self, notification, user, event, position, json=None):
        if user.hasAttribute("notificationTokens"):

            shortMessage = self._notificationFormatter.formatMessage(user, event, position, "short")

            item = self.NotificationObject()
            item.title = shortMessage.getSubject()
            item.body = shortMessage.getBody()
            item.sound = "default"

            tokenArray = user.getString("notificationTokens").split("[, ]")
            registrationTokens = [tokenArray]

            message = self.Message()
            message.tokens = user.getString("notificationTokens").split("[, ]")
            message.notification = item

            request = self._client.target(self._url).request().header("Authorization", "key=" + self._key)
            try:
                with request.post(Entity.json(message)) as result:
                    json = result.readEntity(json.__class__)
                    failedTokens = []
                    responses = json.getJsonArray("responses")
                    for i, unusedItem in enumerate(responses):
                        response = responses.getJsonObject(i)
                        if not response.getBoolean("success"):
                            error = response.getJsonObject("error")
                            errorCode = error.getString("code")
                            if errorCode == "messaging/invalid-argument" or errorCode == "messaging/registration-token-not-registered":
                                failedTokens.append(registrationTokens[i])
                            NotificatorTraccar._LOGGER.warn("Push user {} error - {}", user.getId(), error.getString("message"))
                    if failedTokens:
                        registrationTokens.removeAll(failedTokens)
                        if not registrationTokens:
                            user.getAttributes().remove("notificationTokens")
                        else:
                            user.set("notificationTokens", str.join(",", registrationTokens))
                        self._storage.updateObject(user, Request(Columns.Include("attributes"), Condition.Equals("id", user.getId())))
                        self._cacheManager.updateOrInvalidate(True, user)
            except StorageException as e:
                NotificatorTraccar._LOGGER.warn("Push error", e)
