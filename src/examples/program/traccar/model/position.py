from datetime import date

from src.examples.program.traccar.storage.queryIgnore import QueryIgnore
from src.examples.program.traccar.storage.storageName import StorageName

from .message import Message


class Position(Message):

    KEY_ORIGINAL = "raw"
    KEY_INDEX = "index"
    KEY_HDOP = "hdop"
    KEY_VDOP = "vdop"
    KEY_PDOP = "pdop"
    KEY_SATELLITES = "sat"
    KEY_SATELLITES_VISIBLE = "satVisible"
    KEY_RSSI = "rssi"
    KEY_GPS = "gps"
    KEY_ROAMING = "roaming"
    KEY_EVENT = "event"
    KEY_ALARM = "alarm"
    KEY_STATUS = "status"
    KEY_ODOMETER = "odometer"
    KEY_ODOMETER_SERVICE = "serviceOdometer"
    KEY_ODOMETER_TRIP = "tripOdometer"
    KEY_HOURS = "hours"
    KEY_STEPS = "steps"
    KEY_HEART_RATE = "heartRate"
    KEY_INPUT = "input"
    KEY_OUTPUT = "output"
    KEY_IMAGE = "image"
    KEY_VIDEO = "video"
    KEY_AUDIO = "audio"



    KEY_POWER = "power"
    KEY_BATTERY = "battery"
    KEY_BATTERY_LEVEL = "batteryLevel"
    KEY_FUEL_LEVEL = "fuel"
    KEY_FUEL_USED = "fuelUsed"
    KEY_FUEL_CONSUMPTION = "fuelConsumption"

    KEY_VERSION_FW = "versionFw"
    KEY_VERSION_HW = "versionHw"
    KEY_TYPE = "type"
    KEY_IGNITION = "ignition"
    KEY_FLAGS = "flags"
    KEY_ANTENNA = "antenna"
    KEY_CHARGE = "charge"
    KEY_IP = "ip"
    KEY_ARCHIVE = "archive"
    KEY_DISTANCE = "distance"
    KEY_TOTAL_DISTANCE = "totalDistance"
    KEY_RPM = "rpm"
    KEY_VIN = "vin"
    KEY_APPROXIMATE = "approximate"
    KEY_THROTTLE = "throttle"
    KEY_MOTION = "motion"
    KEY_ARMED = "armed"
    KEY_GEOFENCE = "geofence"
    KEY_ACCELERATION = "acceleration"
    KEY_DEVICE_TEMP = "deviceTemp"
    KEY_COOLANT_TEMP = "coolantTemp"
    KEY_ENGINE_LOAD = "engineLoad"
    KEY_OPERATOR = "operator"
    KEY_COMMAND = "command"
    KEY_BLOCKED = "blocked"
    KEY_LOCK = "lock"
    KEY_DOOR = "door"
    KEY_AXLE_WEIGHT = "axleWeight"
    KEY_G_SENSOR = "gSensor"
    KEY_ICCID = "iccid"
    KEY_PHONE = "phone"
    KEY_SPEED_LIMIT = "speedLimit"
    KEY_DRIVING_TIME = "drivingTime"

    KEY_DTCS = "dtcs"
    KEY_OBD_SPEED = "obdSpeed"
    KEY_OBD_ODOMETER = "obdOdometer"

    KEY_RESULT = "result"

    KEY_DRIVER_UNIQUE_ID = "driverUniqueId"
    KEY_CARD = "card"


    PREFIX_TEMP = "temp"
    PREFIX_ADC = "adc"
    PREFIX_IO = "io"
    PREFIX_COUNT = "count"
    PREFIX_IN = "in"
    PREFIX_OUT = "out"

    ALARM_GENERAL = "general"
    ALARM_SOS = "sos"
    ALARM_VIBRATION = "vibration"
    ALARM_MOVEMENT = "movement"
    ALARM_LOW_SPEED = "lowspeed"
    ALARM_OVERSPEED = "overspeed"
    ALARM_FALL_DOWN = "fallDown"
    ALARM_LOW_POWER = "lowPower"
    ALARM_LOW_BATTERY = "lowBattery"
    ALARM_FAULT = "fault"
    ALARM_POWER_OFF = "powerOff"
    ALARM_POWER_ON = "powerOn"
    ALARM_DOOR = "door"
    ALARM_LOCK = "lock"
    ALARM_UNLOCK = "unlock"
    ALARM_GEOFENCE = "geofence"
    ALARM_GEOFENCE_ENTER = "geofenceEnter"
    ALARM_GEOFENCE_EXIT = "geofenceExit"
    ALARM_GPS_ANTENNA_CUT = "gpsAntennaCut"
    ALARM_ACCIDENT = "accident"
    ALARM_TOW = "tow"
    ALARM_IDLE = "idle"
    ALARM_HIGH_RPM = "highRpm"
    ALARM_ACCELERATION = "hardAcceleration"
    ALARM_BRAKING = "hardBraking"
    ALARM_CORNERING = "hardCornering"
    ALARM_LANE_CHANGE = "laneChange"
    ALARM_FATIGUE_DRIVING = "fatigueDriving"
    ALARM_POWER_CUT = "powerCut"
    ALARM_POWER_RESTORED = "powerRestored"
    ALARM_JAMMING = "jamming"
    ALARM_TEMPERATURE = "temperature"
    ALARM_PARKING = "parking"
    ALARM_BONNET = "bonnet"
    ALARM_FOOT_BRAKE = "footBrake"
    ALARM_FUEL_LEAK = "fuelLeak"
    ALARM_TAMPERING = "tampering"
    ALARM_REMOVING = "removing"

    def __init__(self):

        self._protocol = None
        self._serverTime = date()
        self._deviceTime = None
        self._fixTime = None
        self._outdated = False
        self._valid = False
        self._latitude = 0
        self._longitude = 0
        self._altitude = 0
        self._speed = 0
        self._course = 0
        self._address = None
        self._accuracy = 0
        self._network = None
        self._geofenceIds = None





    def __init__(self, protocol):
        self._protocol = protocol

    def getProtocol(self):
        return self._protocol

    def setProtocol(self, protocol):
        self._protocol = protocol

    def getServerTime(self):
        return self._serverTime

    def setServerTime(self, serverTime):
        self._serverTime = serverTime

    def getDeviceTime(self):
        return self._deviceTime

    def setDeviceTime(self, deviceTime):
        self._deviceTime = deviceTime

    def getFixTime(self):
        return self._fixTime

    def setFixTime(self, fixTime):
        self._fixTime = fixTime



    def setTime(self, time):
        self.setDeviceTime(time)
        self.setFixTime(time)



    def getOutdated(self):
        return self._outdated



    def setOutdated(self, outdated):
        self._outdated = outdated

    def getValid(self):
        return self._valid

    def setValid(self, valid):
        self._valid = valid

    def getLatitude(self):
        return self._latitude

    def setLatitude(self, latitude):
        if latitude < -90 or latitude > 90:
            raise Exception("Latitude out of range")
        self._latitude = latitude

    def getLongitude(self):
        return self._longitude

    def setLongitude(self, longitude):
        if longitude < -180 or longitude > 180:
            raise Exception("Longitude out of range")
        self._longitude = longitude

    def getAltitude(self):
        return self._altitude

    def setAltitude(self, altitude):
        self._altitude = altitude

    def getSpeed(self):
        return self._speed

    def setSpeed(self, speed):
        self._speed = speed

    def getCourse(self):
        return self._course

    def setCourse(self, course):
        self._course = course

    def getAddress(self):
        return self._address

    def setAddress(self, address):
        self._address = address

    def getAccuracy(self):
        return self._accuracy

    def setAccuracy(self, accuracy):
        self._accuracy = accuracy

    def getNetwork(self):
        return self._network

    def setNetwork(self, network):
        self._network = network

    def getGeofenceIds(self):
        return self._geofenceIds

    def setGeofenceIds(self, geofenceIds):
        if geofenceIds is not None:
            self._geofenceIds = geofenceIds.stream().map("longValue")
        else:
            self._geofenceIds = None



    def getType(self):
        return super().getType()



    def setType(self, type):
        super().setType(type)


