from xml.dom.minidom import Entity

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.notification import Notification
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.notification.notificationFormatter import NotificationFormatter

import math

from src.examples.program.traccar.notificators.notificator import Notificator


class NotificatorTelegram(Notificator):



    class TextMessage:

        def __init__(self):

            self._chatId = None
            self._text = None
            self._parseMode = "html"


    class LocationMessage:

        def __init__(self):

            self._chatId = None
            self._latitude = 0
            self._longitude = 0
            self._accuracy = 0
            self._bearing = 0


    def __init__(self, config, notificationFormatter, client):

        self._notificationFormatter = None
        self._client = None
        self._urlSendText = None
        self._urlSendLocation = None
        self._chatId = None
        self._sendLocation = False

        self._notificationFormatter = notificationFormatter
        self._client = client
        self._urlSendText = "https://api.telegram.org/bot{0}/sendMessage".format(config.getString(Keys.NOTIFICATOR_TELEGRAM_KEY))
        self._urlSendLocation = "https://api.telegram.org/bot{0}/sendLocation".format(config.getString(Keys.NOTIFICATOR_TELEGRAM_KEY))
        self._chatId = config.getString(Keys.NOTIFICATOR_TELEGRAM_CHAT_ID)
        self._sendLocation = config.getBoolean(Keys.NOTIFICATOR_TELEGRAM_SEND_LOCATION)

    def _createLocationMessage(self, messageChatId, position):
        locationMessage = self.LocationMessage()
        locationMessage.chatId = messageChatId
        locationMessage.latitude = position.getLatitude()
        locationMessage.longitude = position.getLongitude()
        locationMessage.bearing = int(math.ceil(position.getCourse()))
        locationMessage.accuracy = position.getAccuracy()
        return locationMessage

    def send(self, notification, user, event, position):
        shortMessage = self._notificationFormatter.formatMessage(user, event, position, "short")

        message = self.TextMessage()
        message.chatId = user.getString("telegramChatId")
        if message.chatId is None:
            message.chatId = self._chatId
        message.text = shortMessage.getBody()
        self._client.target(self._urlSendText).request().post(Entity.json(message)).close()
        if self._sendLocation and position is not None:
            self._client.target(self._urlSendLocation).request().post(Entity.json(self._createLocationMessage(message.chatId, position))).close()
