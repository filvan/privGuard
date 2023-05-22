from src.examples.program.traccar.storage.storageName import StorageName
from .extendedModel import ExtendedModel
class Driver(ExtendedModel):

    def __init__(self):
        #instance fields found by Java to Python Converter:
        self._name = None
        self._uniqueId = None



    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name


    def getUniqueId(self):
        return self._uniqueId

    def setUniqueId(self, uniqueId):
        self._uniqueId = uniqueId
