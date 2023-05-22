from src.examples.program.traccar.model.baseModel import BaseModel
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position


class BroadcastMessage:

    def __init__(self):
        #instance fields found by Java to Python Converter:
        self._device = None
        self._position = None
        self._userId = 0
        self._event = None
        self._commandDeviceId = 0
        self._changes = None



    def getDevice(self):
        return self._device

    def setDevice(self, device):
        self._device = device


    def getPosition(self):
        return self._position

    def setPosition(self, position):
        self._position = position


    def getUserId(self):
        return self._userId

    def setUserId(self, userId):
        self._userId = userId


    def getEvent(self):
        return self._event

    def setEvent(self, event):
        self._event = event


    def getCommandDeviceId(self):
        return self._commandDeviceId

    def setCommandDeviceId(self, commandDeviceId):
        self._commandDeviceId = commandDeviceId


    def getChanges(self):
        return self._changes

    def setChanges(self, changes):
        self._changes = changes
