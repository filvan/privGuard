from src.examples.program.traccar.mail.mailManager import MailManager
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.notification import Notification
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.notification.messageException import MessageException
from src.examples.program.traccar.notification.notificationFormatter import NotificationFormatter
from src.examples.program.traccar.notificators.notificator import Notificator


class NotificatorMail(Notificator):


    def __init__(self, mailManager, notificationFormatter):

        self._mailManager = None
        self._notificationFormatter = None

        self._mailManager = mailManager
        self._notificationFormatter = notificationFormatter

    def send(self, notification, user, event, position):
        try:
            fullMessage = self._notificationFormatter.formatMessage(user, event, position, "full")
            self._mailManager.sendMessage(user, False, fullMessage.getSubject(), fullMessage.getBody())
        except MessageException as e:
            raise MessageException(e)
