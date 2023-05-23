import sys

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.handler.ackowledgementHandler import AcknowledgementHandler
from src.examples.program.traccar.helper.unitsConverter import UnitsConverter
from src.examples.program.traccar.helper.model.attributeUtil import AttributeUtil
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.cache.cacheManager import CacheManager
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.order import Order
from src.examples.program.traccar.storage.query.request import Request


class FilterHandler():

    _LOGGER = "LoggerFactory.getLogger(FilterHandler.class)"


    def __init__(self, config, cacheManager, storage):

        self._enabled = False
        self._filterInvalid = False
        self._filterZero = False
        self._filterDuplicate = False
        self._filterOutdated = False
        self._filterFuture = 0
        self._filterPast = 0
        self._filterApproximate = False
        self._filterAccuracy = 0
        self._filterStatic = False
        self._filterDistance = 0
        self._filterMaxSpeed = 0
        self._filterMinPeriod = 0
        self._filterRelative = False
        self._skipLimit = 0
        self._skipAttributes = False
        self._cacheManager = None
        self._storage = None

        self._enabled = config.getBoolean(Keys.FILTER_ENABLE)
        self._filterInvalid = config.getBoolean(Keys.FILTER_INVALID)
        self._filterZero = config.getBoolean(Keys.FILTER_ZERO)
        self._filterDuplicate = config.getBoolean(Keys.FILTER_DUPLICATE)
        self._filterOutdated = config.getBoolean(Keys.FILTER_OUTDATED)
        self._filterFuture = config.getLong(Keys.FILTER_FUTURE) * 1000
        self._filterPast = config.getLong(Keys.FILTER_PAST) * 1000
        self._filterAccuracy = config.getInteger(Keys.FILTER_ACCURACY)
        self._filterApproximate = config.getBoolean(Keys.FILTER_APPROXIMATE)
        self._filterStatic = config.getBoolean(Keys.FILTER_STATIC)
        self._filterDistance = config.getInteger(Keys.FILTER_DISTANCE)
        self._filterMaxSpeed = config.getInteger(Keys.FILTER_MAX_SPEED)
        self._filterMinPeriod = config.getInteger(Keys.FILTER_MIN_PERIOD) * 1000
        self._filterRelative = config.getBoolean(Keys.FILTER_RELATIVE)
        self._skipLimit = config.getLong(Keys.FILTER_SKIP_LIMIT) * 1000
        self._skipAttributes = config.getBoolean(Keys.FILTER_SKIP_ATTRIBUTES_ENABLE)
        self._cacheManager = cacheManager
        self._storage = storage
    def _getPrecedingPosition(self, deviceId, date):
        return self._storage.getObject(Position.__class__, Request(Columns.All(), Condition.And(Condition.Equals("deviceId", deviceId), Condition.Compare("fixTime", "<=", "time", date)), Order("fixTime", True, 1)))

    def _filterInvalid(self, position):
        return self._filterInvalid and ((not position.getValid()) or position.getLatitude() > 90 or position.getLongitude() > 180 or position.getLatitude() < -90 or position.getLongitude() < -180)

    def _filterZero(self, position):
        return self._filterZero and position.getLatitude() == 0.0 and position.getLongitude() == 0.0

    def _filterDuplicate(self, position, last):
        if self._filterDuplicate and last is not None and position.getFixTime() is last.getFixTime():
            for key in position.getAttributes().keySet():
                if not last.hasAttribute(key):
                    return False
            return True
        return False

    def _filterOutdated(self, position):
        return self._filterOutdated and position.getOutdated()

    def _filterFuture(self, position):
        return self._filterFuture != 0 and position.getFixTime().getTime() > sys.currentTimeMillis() + self._filterFuture

    def _filterPast(self, position):
        return self._filterPast != 0 and position.getFixTime().getTime() < sys.currentTimeMillis() - self._filterPast

    def _filterAccuracy(self, position):
        return self._filterAccuracy != 0 and position.getAccuracy() > self._filterAccuracy

    def _filterApproximate(self, position):
        return self._filterApproximate and position.getBoolean(Position.KEY_APPROXIMATE)

    def _filterStatic(self, position):
        return self._filterStatic and position.getSpeed() == 0.0

    def _filterDistance(self, position, last):
        if self._filterDistance != 0 and last is not None:
            return position.getDouble(Position.KEY_DISTANCE) < self._filterDistance
        return False

    def _filterMaxSpeed(self, position, last):
        if self._filterMaxSpeed != 0 and last is not None:
            distance = position.getDouble(Position.KEY_DISTANCE)
            time = position.getFixTime().getTime() - last.getFixTime().getTime()
            return UnitsConverter.knotsFromMps(distance / (time / 1000)) > self._filterMaxSpeed
        return False

    def _filterMinPeriod(self, position, last):
        if self._filterMinPeriod != 0 and last is not None:
            time = position.getFixTime().getTime() - last.getFixTime().getTime()
            return time > 0 and time < self._filterMinPeriod
        return False

    def _skipLimit(self, position, last):
        if self._skipLimit != 0 and last is not None:
            return (position.getServerTime().getTime() - last.getServerTime().getTime()) > self._skipLimit
        return False

    def _skipAttributes(self, position):
        if self._skipAttributes:
            string = AttributeUtil.lookup(self._cacheManager, Keys.FILTER_SKIP_ATTRIBUTES, position.getDeviceId())
            for attribute in string.split("[ ,]"):
                if position.hasAttribute(attribute):
                    return True
        return False

    def filter(self, position):

        filterType = ""


        if self._filterInvalid(position):
            filterType.append("Invalid ")
        if self._filterZero(position):
            filterType.append("Zero ")
        if self._filterOutdated(position):
            filterType.append("Outdated ")
        if self._filterFuture(position):
            filterType.append("Future ")
        if self._filterPast(position):
            filterType.append("Past ")
        if self._filterAccuracy(position):
            filterType.append("Accuracy ")
        if self._filterApproximate(position):
            filterType.append("Approximate ")


        deviceId = position.getDeviceId()
        if self._filterDuplicate or self._filterStatic or self._filterDistance > 0 or self._filterMaxSpeed > 0 or self._filterMinPeriod > 0:
            preceding = None
            if self._filterRelative:
                try:
                    newFixTime = position.getFixTime()
                    preceding = self._getPrecedingPosition(deviceId, newFixTime)
                except StorageException as e:
                    self._LOGGER.warn("Error retrieving preceding position; fallbacking to last received position.", e)
                    preceding = self._cacheManager.getPosition(deviceId)
            else:
                preceding = self._cacheManager.getPosition(deviceId)
            if self._filterDuplicate(position, preceding) and (not self._skipLimit(position, preceding)) and not self._skipAttributes(
                    position):
                filterType.append("Duplicate ")
            if self._filterStatic(position) and (not self._skipLimit(position, preceding)) and not self._skipAttributes(position):
                filterType.append("Static ")
            if self._filterDistance(position, preceding) and (not self._skipLimit(position, preceding)) and not self._skipAttributes(
                    position):
                filterType.append("Distance ")
            if self._filterMaxSpeed(position, preceding):
                filterType.append("MaxSpeed ")
            if self._filterMinPeriod(position, preceding):
                filterType.append("MinPeriod ")

        if filterType.length() > 0:
            uniqueId = self._cacheManager.getObject(Device.__class__, deviceId).getUniqueId()
            self._LOGGER.info("Position filtered by {}filters from device: {}", filterType, uniqueId)

            return True

        return False

    def channelRead(self, ctx, msg):
        if isinstance(msg, Position):
            position = msg
            if self._enabled and self.filter(position):
                ctx.writeAndFlush(AcknowledgementHandler.EventHandled(position))
            else:
                ctx.fireChannelRead(position)
        else:
            super().channelRead(ctx, msg)


