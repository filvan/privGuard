from .groupModel import GroupedModel
from src.examples.program.traccar.storage.storageName import StorageName

class Group(GroupedModel):

    def __init__(self):
        #instance fields found by Java to Python Converter:
        self._name = None



    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name
