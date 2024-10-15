from datetime import date

from src.examples.program.traccar.storage.storageName import StorageName
from .message import Message


class Event(Message):

    def _initialize_instance_fields(self):
        self._eventTime = None
        self._positionId = 0
        self._geofenceId = 0
        self._maintenanceId = 0

    def __init__(self, type, position):
        super().__init__()
        self._initialize_instance_fields()

        Message.setType(type)
        self.setPositionId(position.getId())
        Message.setDeviceId(position.getDeviceId())
        self._eventTime = position.getDeviceTime()

    def __init__(self, type, deviceId):
        self._initialize_instance_fields()

        Message.setType(type)
        Message.setDeviceId(deviceId)
        self._eventTime = date()

    def __init__(self):
        self._initialize_instance_fields()

    ALL_EVENTS = "allEvents"

    TYPE_COMMAND_RESULT = "commandResult"

    TYPE_DEVICE_ONLINE = "deviceOnline"
    TYPE_DEVICE_UNKNOWN = "deviceUnknown"
    TYPE_DEVICE_OFFLINE = "deviceOffline"
    TYPE_DEVICE_INACTIVE = "deviceInactive"

    TYPE_DEVICE_MOVING = "deviceMoving"
    TYPE_DEVICE_STOPPED = "deviceStopped"

    TYPE_DEVICE_OVERSPEED = "deviceOverspeed"
    TYPE_DEVICE_FUEL_DROP = "deviceFuelDrop"
    TYPE_DEVICE_FUEL_INCREASE = "deviceFuelIncrease"

    TYPE_GEOFENCE_ENTER = "geofenceEnter"
    TYPE_GEOFENCE_EXIT = "geofenceExit"

    TYPE_ALARM = "alarm"

    TYPE_IGNITION_ON = "ignitionOn"
    TYPE_IGNITION_OFF = "ignitionOff"

    TYPE_MAINTENANCE = "maintenance"
    TYPE_TEXT_MESSAGE = "textMessage"
    TYPE_DRIVER_CHANGED = "driverChanged"
    TYPE_MEDIA = "media"

    def getEventTime(self):
        return self._eventTime

    def setEventTime(self, eventTime):
        self._eventTime = eventTime

    def getPositionId(self):
        return self._positionId

    def setPositionId(self, positionId):
        self._positionId = positionId

    def getGeofenceId(self):
        return self._geofenceId

    def setGeofenceId(self, geofenceId):
        self._geofenceId = geofenceId

    def getMaintenanceId(self):
        return self._maintenanceId

    def setMaintenanceId(self, maintenanceId):
        self._maintenanceId = maintenanceId
