from src.examples.program.traccar.database.statisticManager import StatisticsManager
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.notification import Notification
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.notification.messageException import MessageException
from src.examples.program.traccar.notification.notificationFormatter import NotificationFormatter
from src.examples.program.traccar.notificators.notificator import Notificator
from src.examples.program.traccar.sms.smsManager import SmsManager

class NotificatorSms(Notificator):


    def __init__(self, smsManager, notificationFormatter, statisticsManager):

        self._smsManager = None
        self._notificationFormatter = None
        self._statisticsManager = None

        self._smsManager = smsManager
        self._notificationFormatter = notificationFormatter
        self._statisticsManager = statisticsManager

    def send(self, notification, user, event, position):
        if user.getPhone() is not None:
            shortMessage = self._notificationFormatter.formatMessage(user, event, position, "short")
            self._statisticsManager.registerSms()
            self._smsManager.sendMessage(user.getPhone(), shortMessage.getBody(), False)
