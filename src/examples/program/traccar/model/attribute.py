from src.examples.program.traccar.storage.storageName import StorageName
from .baseModel import BaseModel
class Attribute(BaseModel):

    def __init__(self):
        #instance fields found by Java to Python Converter:
        self._description = None
        self._attribute = None
        self._expression = None
        self._type = None



    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description


    def getAttribute(self):
        return self._attribute

    def setAttribute(self, attribute):
        self._attribute = attribute


    def getExpression(self):
        return self._expression

    def setExpression(self, expression):
        self._expression = expression


    def getType(self):
        return self._type

    def setType(self, type):
        self._type = type
