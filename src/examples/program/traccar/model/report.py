from src.examples.program.traccar.storage.storageName import StorageName
from .schedulable import Schedulable


class Report(Schedulable):

    def __init__(self):
        super().__init__()
        self._type = None
        self._description = None

    def getType(self):
        return self._type

    def setType(self, type):
        self._type = type

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description
