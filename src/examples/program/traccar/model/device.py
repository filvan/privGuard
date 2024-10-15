from src.examples.program.traccar.storage.queryIgnore import QueryIgnore
from src.examples.program.traccar.storage.storageName import StorageName
from .groupedModel import GroupedModel
from .disableable import Disableable


class Device(GroupedModel, Disableable):

    def __init__(self):
        super().__init__()
        self._name = None
        self._uniqueId = None
        self._status = None
        self._lastUpdate = None
        self._positionId = 0
        self._phone = None
        self._model = None
        self._contact = None
        self._category = None
        self._disabled = False
        self._expirationTime = None
        self._motionStreak = False
        self._motionState = False
        self._motionTime = None
        self._motionDistance = 0
        self._overspeedState = False
        self._overspeedTime = None
        self._overspeedGeofenceId = 0

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getUniqueId(self):
        return self._uniqueId

    def setUniqueId(self, uniqueId):
        self._uniqueId = uniqueId

    STATUS_UNKNOWN = "unknown"
    STATUS_ONLINE = "online"
    STATUS_OFFLINE = "offline"

    def getStatus(self):
        return self._status if self._status is not None else Device.STATUS_OFFLINE

    def setStatus(self, status):
        self._status = status.trim() if status is not None else None

    def getLastUpdate(self):
        return self._lastUpdate

    def setLastUpdate(self, lastUpdate):
        self._lastUpdate = lastUpdate

    def getPositionId(self):
        return self._positionId

    def setPositionId(self, positionId):
        self._positionId = positionId

    def getPhone(self):
        return self._phone

    def setPhone(self, phone):
        self._phone = phone

    def getModel(self):
        return self._model

    def setModel(self, model):
        self._model = model

    def getContact(self):
        return self._contact

    def setContact(self, contact):
        self._contact = contact

    def getCategory(self):
        return self._category

    def setCategory(self, category):
        self._category = category

    def getDisabled(self):
        return self._disabled

    def setDisabled(self, disabled):
        self._disabled = disabled

    def getExpirationTime(self):
        return self._expirationTime

    def setExpirationTime(self, expirationTime):
        self._expirationTime = expirationTime

    def getMotionStreak(self):
        return self._motionStreak

    def setMotionStreak(self, motionStreak):
        self._motionStreak = motionStreak

    def getMotionState(self):
        return self._motionState

    def setMotionState(self, motionState):
        self._motionState = motionState

    def getMotionTime(self):
        return self._motionTime

    def setMotionTime(self, motionTime):
        self._motionTime = motionTime

    def getMotionDistance(self):
        return self._motionDistance

    def setMotionDistance(self, motionDistance):
        self._motionDistance = motionDistance

    def getOverspeedState(self):
        return self._overspeedState

    def setOverspeedState(self, overspeedState):
        self._overspeedState = overspeedState

    def getOverspeedTime(self):
        return self._overspeedTime

    def setOverspeedTime(self, overspeedTime):
        self._overspeedTime = overspeedTime

    def getOverspeedGeofenceId(self):
        return self._overspeedGeofenceId

    def setOverspeedGeofenceId(self, overspeedGeofenceId):
        self._overspeedGeofenceId = overspeedGeofenceId
