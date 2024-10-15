from numpy import array

from src.examples.program.traccar.storage.queryIgnore import QueryIgnore
from src.examples.program.traccar.storage.storageName import StorageName
from .schedulable import Schedulable


class Notification(Schedulable):

    def __init__(self):

        super().__init__()
        self._always = False
        self._type = None
        self._commandId = 0
        self._notificators = None

    def getAlways(self):
        return self._always

    def setAlways(self, always):
        self._always = always

    def getType(self):
        return self._type

    def setType(self, type):
        self._type = type

    def getCommandId(self):
        return self._commandId

    def setCommandId(self, commandId):
        self._commandId = commandId

    def getNotificators(self):
        return self._notificators

    def setNotificators(self, transports):
        self._notificators = transports

    def getNotificatorsTypes(self):
        result = array()
        if self._notificators is not None:
            transportsList = self._notificators.split(",")
            for transport in transportsList:
                result.add(transport.trim())
        return result
