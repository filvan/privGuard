from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.device import Device

class OverspeedState:

    def __init__(self):
        #instance fields found by Java to Python Converter:
        self._changed = False
        self._overspeedState = False
        self._overspeedTime = None
        self._overspeedGeofenceId = 0
        self._event = None


    @staticmethod
    def fromDevice(device):
        state = OverspeedState()
        state._overspeedState = device.getOverspeedState()
        state._overspeedTime = device.getOverspeedTime()
        state._overspeedGeofenceId = device.getOverspeedGeofenceId()
        return state

    def toDevice(self, device):
        device.setOverspeedState(self._overspeedState)
        device.setOverspeedTime(self._overspeedTime)
        device.setOverspeedGeofenceId(self._overspeedGeofenceId)


    def isChanged(self):
        return self._changed


    def getOverspeedState(self):
        return self._overspeedState

    def setOverspeedState(self, overspeedState):
        self._overspeedState = overspeedState
        self._changed = True


    def getOverspeedTime(self):
        return self._overspeedTime

    def setOverspeedTime(self, overspeedTime):
        self._overspeedTime = overspeedTime
        self._changed = True


    def getOverspeedGeofenceId(self):
        return self._overspeedGeofenceId

    def setOverspeedGeofenceId(self, overspeedGeofenceId):
        self._overspeedGeofenceId = overspeedGeofenceId
        self._changed = True


    def getEvent(self):
        return self._event

    def setEvent(self, event):
        self._event = event
