from src.examples.program.traccar.model.baseModel import BaseModel
class CacheValue:


    def __init__(self, value):
        self._value = None
        self._references = []

        self._value = value

    def retain(self, deviceId):
        self._references.add(deviceId)

    def release(self, deviceId):
        self._references.remove(deviceId)

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value

    def getReferences(self):
        return self._references
