from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.event import Event

class MotionState:

    def __init__(self):
        self._changed = False
        self._motionStreak = False
        self._motionState = False
        self._motionTime = None
        self._motionDistance = 0
        self._event = None


    @staticmethod
    def fromDevice(device):
        state = MotionState()
        state._motionStreak = device.getMotionStreak()
        state._motionState = device.getMotionState()
        state._motionTime = device.getMotionTime()
        state._motionDistance = device.getMotionDistance()
        return state

    def toDevice(self, device):
        device.setMotionStreak(self._motionStreak)
        device.setMotionState(self._motionState)
        device.setMotionTime(self._motionTime)
        device.setMotionDistance(self._motionDistance)


    def isChanged(self):
        return self._changed


    def getMotionStreak(self):
        return self._motionStreak

    def setMotionStreak(self, motionStreak):
        self._motionStreak = motionStreak
        self._changed = True


    def getMotionState(self):
        return self._motionState

    def setMotionState(self, motionState):
        self._motionState = motionState
        self._changed = True


    def getMotionTime(self):
        return self._motionTime

    def setMotionTime(self, motionTime):
        self._motionTime = motionTime
        self._changed = True


    def getMotionDistance(self):
        return self._motionDistance

    def setMotionDistance(self, motionDistance):
        self._motionDistance = motionDistance
        self._changed = True


    def getEvent(self):
        return self._event

    def setEvent(self, event):
        self._event = event
