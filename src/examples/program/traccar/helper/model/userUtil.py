import sys
from datetime import date

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.configKey import ConfigKey
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.model.server import Server

from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.order import Order
from src.examples.program.traccar.storage.query.request import Request

class UserUtil:

    def __init__(self):
        pass

    def isEmpty(storage):
        return storage.getObjects(User.__class__, Request(Columns.Include("id"), Order("id", False, 1))).isEmpty()

    def getDistanceUnit(server, user):
        return UserUtil._lookupStringAttribute(server, user, "distanceUnit", "km")

    def getSpeedUnit(server, user):
        return UserUtil._lookupStringAttribute(server, user, "speedUnit", "kn")

    def getVolumeUnit(server, user):
        return UserUtil._lookupStringAttribute(server, user, "volumeUnit", "ltr")

    def getTimezone(server, user):
        timezone = UserUtil._lookupStringAttribute(server, user, "timezone", None)
        return timezone.getTimeZone(timezone) if timezone is not None else timezone.getDefault()

    def _lookupStringAttribute(server, user, key, defaultValue):
        preference = None
        serverPreference = server.getString(key)
        userPreference = user.getString(key)
        if server.getForceSettings():
            preference = serverPreference if serverPreference is not None else userPreference
        else:
            preference = userPreference if userPreference is not None else serverPreference
        return preference if preference is not None else defaultValue

    def setUserDefaults(user, config):
        user.setDeviceLimit(config.getInteger(Keys.USERS_DEFAULT_DEVICE_LIMIT))
        expirationDays = config.getInteger(Keys.USERS_DEFAULT_EXPIRATION_DAYS)
        if expirationDays > 0:
            user.setExpirationTime(date(sys.currentTimeMillis() + expirationDays * 86400000))

