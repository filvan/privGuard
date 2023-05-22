from src.examples.program.traccar.model.baseModel import BaseModel
from collections import OrderedDict
class ExtendedModel(BaseModel):

    def __init__(self):

        self._attributes = OrderedDict()



    def hasAttribute(self, key):
        return key in self._attributes.keys()

    def getAttributes(self):
        return self._attributes

    def setAttributes(self, attributes):
        self._attributes = OrderedDict(attributes)

    def set(self, key, value):
        if value is not None:
            self._attributes[key] = value

    def set(self, key, value):
        if value is not None:
            self._attributes[key] = int(value)

    def set(self, key, value):
        if value is not None:
            self._attributes[key] = int(value)

    def set(self, key, value):
        if value is not None:
            self._attributes[key] = value

    def set(self, key, value):
        if value is not None:
            self._attributes[key] = value

    def set(self, key, value):
        if value is not None:
            self._attributes[key] = float(value)

    def set(self, key, value):
        if value is not None:
            self._attributes[key] = value

    def set(self, key, value):
        if value is not None and value:
            self._attributes[key] = value

    def add(self, entry):
        if entry is not None and entry.getValue() is not None:
            self._attributes[entry.getKey()] = entry.getValue()

    def getString(self, key, defaultValue):
        if key in self._attributes.keys():
            return str(self._attributes[key])
        else:
            return defaultValue

    def getString(self, key):
        return self.getString(key, None)

    def getDouble(self, key):
        if key in self._attributes.keys():
            value = self._attributes[key]
            if isinstance(value, float) | isinstance(value,int):
                return (self._attributes[key]).doubleValue()
            else:
                return float(str(value))
        else:
            return 0.0

    def getBoolean(self, key):
        if key in self._attributes.keys():
            value = self._attributes[key]
            if isinstance(value, bool):
                return bool(self._attributes[key])
            else:
                return bool(str(value))
        else:
            return False

    def getInteger(self, key):
        if key in self._attributes.keys():
            value = self._attributes[key]
            if isinstance(value, int):
                return (self._attributes[key]).intValue()
            else:
                return int(str(value))
        else:
            return 0

    def getLong(self, key):
        if key in self._attributes.keys():
            value = self._attributes[key]
            if isinstance(value, int):
                return (self._attributes[key]).longValue()
            else:
                return int(str(value))
        else:
            return 0
