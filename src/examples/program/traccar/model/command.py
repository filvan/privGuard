from src.examples.program.traccar.storage.queryIgnore import QueryIgnore
from src.examples.program.traccar.storage.storageName import StorageName
from .baseCommand import BaseCommand


class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self._description = None

    TYPE_CUSTOM = "custom"
    TYPE_IDENTIFICATION = "deviceIdentification"
    TYPE_POSITION_SINGLE = "positionSingle"
    TYPE_POSITION_PERIODIC = "positionPeriodic"
    TYPE_POSITION_STOP = "positionStop"
    TYPE_ENGINE_STOP = "engineStop"
    TYPE_ENGINE_RESUME = "engineResume"
    TYPE_ALARM_ARM = "alarmArm"
    TYPE_ALARM_DISARM = "alarmDisarm"
    TYPE_ALARM_DISMISS = "alarmDismiss"
    TYPE_SET_TIMEZONE = "setTimezone"
    TYPE_REQUEST_PHOTO = "requestPhoto"
    TYPE_POWER_OFF = "powerOff"
    TYPE_REBOOT_DEVICE = "rebootDevice"
    TYPE_FACTORY_RESET = "factoryReset"
    TYPE_SEND_SMS = "sendSms"
    TYPE_SEND_USSD = "sendUssd"
    TYPE_SOS_NUMBER = "sosNumber"
    TYPE_SILENCE_TIME = "silenceTime"
    TYPE_SET_PHONEBOOK = "setPhonebook"
    TYPE_MESSAGE = "message"
    TYPE_VOICE_MESSAGE = "voiceMessage"
    TYPE_OUTPUT_CONTROL = "outputControl"
    TYPE_VOICE_MONITORING = "voiceMonitoring"
    TYPE_SET_AGPS = "setAgps"
    TYPE_SET_INDICATOR = "setIndicator"
    TYPE_CONFIGURATION = "configuration"
    TYPE_GET_VERSION = "getVersion"
    TYPE_FIRMWARE_UPDATE = "firmwareUpdate"
    TYPE_SET_CONNECTION = "setConnection"
    TYPE_SET_ODOMETER = "setOdometer"
    TYPE_GET_MODEM_STATUS = "getModemStatus"
    TYPE_GET_DEVICE_STATUS = "getDeviceStatus"
    TYPE_SET_SPEED_LIMIT = "setSpeedLimit"
    TYPE_MODE_POWER_SAVING = "modePowerSaving"
    TYPE_MODE_DEEP_SLEEP = "modeDeepSleep"

    TYPE_ALARM_GEOFENCE = "alarmGeofence"
    TYPE_ALARM_BATTERY = "alarmBattery"
    TYPE_ALARM_SOS = "alarmSos"
    TYPE_ALARM_REMOVE = "alarmRemove"
    TYPE_ALARM_CLOCK = "alarmClock"
    TYPE_ALARM_SPEED = "alarmSpeed"
    TYPE_ALARM_FALL = "alarmFall"
    TYPE_ALARM_VIBRATION = "alarmVibration"

    KEY_UNIQUE_ID = "uniqueId"
    KEY_FREQUENCY = "frequency"
    KEY_LANGUAGE = "language"
    KEY_TIMEZONE = "timezone"
    KEY_DEVICE_PASSWORD = "devicePassword"
    KEY_RADIUS = "radius"
    KEY_MESSAGE = "message"
    KEY_ENABLE = "enable"
    KEY_DATA = "data"
    KEY_INDEX = "index"
    KEY_PHONE = "phone"
    KEY_SERVER = "server"
    KEY_PORT = "port"

    def getDeviceId(self):
        return super().getDeviceId()

    def setDeviceId(self, deviceId):
        super().setDeviceId(deviceId)

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description
