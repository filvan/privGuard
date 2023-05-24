from xml.dom.minidom import Entity

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.notification import Notification
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.notification.notificationFormatter import NotificationFormatter
from src.examples.program.traccar.notificators.notificator import Notificator


class NotificatorPushover(Notificator):



    class Message:

        def __init__(self):

            self._token = None
            self._user = None
            self._device = None
            self._title = None
            self._message = None


    def __init__(self, config, notificationFormatter, client):

        self._notificationFormatter = None
        self._client = None
        self._url = None
        self._token = None
        self._user = None

        self._notificationFormatter = notificationFormatter
        self._client = client
        self._url = "https://api.pushover.net/1/messages.json"
        self._token = config.getString(Keys.NOTIFICATOR_PUSHOVER_TOKEN)
        self._user = config.getString(Keys.NOTIFICATOR_PUSHOVER_USER)

    def send(self, notification, user, event, position):
        shortMessage = self._notificationFormatter.formatMessage(user, event, position, "short")

        message = self.Message()
        message.token = self._token

        message.user = user.getString("pushoverUserKey")
        if message.user is None:
            message.user = self._user

        if user.hasAttribute("pushoverDeviceNames"):
            message.device = user.getString("pushoverDeviceNames").replaceAll(" *, *", ",")

        message.title = shortMessage.getSubject()
        message.message = shortMessage.getBody()

        self._client.target(self._url).request().post(Entity.json(message)).close()
