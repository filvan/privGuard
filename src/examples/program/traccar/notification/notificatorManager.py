import collections

from numpy import array

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.model.typed import Typed
from src.examples.program.traccar.notificators.notificator import Notificator
from src.examples.program.traccar.notificators.notificatorCommand import NotificatorCommand
from src.examples.program.traccar.notificators.notificatorMail import NotificationFormatter
from src.examples.program.traccar.notificators.notificatorFirebase import NotificatorFirebase
from src.examples.program.traccar.notificators.notificatorMail import NotificatorMail
from src.examples.program.traccar.notificators.notificatorPushover import NotificatorPushover
from src.examples.program.traccar.notificators.notificatorSms import NotificatorSms
from src.examples.program.traccar.notificators.notificatorTelegram import NotificatorTelegram
from src.examples.program.traccar.notificators.notificatorWeb import NotificatorWeb
from src.examples.program.traccar.notificators.notificatorTraccar import NotificatorTraccar

class NotificatorManager:

    _NOTIFICATORS_ALL = { "command": NotificatorCommand.__class__, "web": NotificatorWeb.__class__, "mail": NotificatorMail.__class__, "sms": NotificatorSms.__class__, "firebase": NotificatorFirebase.__class__, "traccar": NotificatorTraccar.__class__, "telegram": NotificatorTelegram.__class__, "pushover": NotificatorPushover.__class__ }



    def __init__(self, injector, config):

        self._injector = None
        self._types = array()

        self._injector = injector
        types = config.getString(Keys.NOTIFICATOR_TYPES)
        if types is not None:
            self._types.addAll((types.split(",")))

    def getNotificator(self, type):
        clazz = NotificatorManager._NOTIFICATORS_ALL[type]
        if clazz is not None:
            notificator = self._injector.getInstance(clazz)
            if notificator is not None:
                return notificator
        raise Exception("Failed to get notificator " + type)

    def getAllNotificatorTypes(self):
        return self._types.stream().map(Typed()).collect(collections.toUnmodifiableSet())
