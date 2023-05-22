from src.examples.program.traccar.storage.storageName import StorageName

from .extendedModel import ExtendedModel

class Order(ExtendedModel):

    def __init__(self):

        self._uniqueId = None
        self._description = None
        self._fromAddress = None
        self._toAddress = None



    def getUniqueId(self):
        return self._uniqueId

    def setUniqueId(self, uniqueId):
        self._uniqueId = uniqueId


    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description


    def getFromAddress(self):
        return self._fromAddress

    def setFromAddress(self, fromAddress):
        self._fromAddress = fromAddress


    def getToAddress(self):
        return self._toAddress

    def setToAddress(self, toAddress):
        self._toAddress = toAddress
