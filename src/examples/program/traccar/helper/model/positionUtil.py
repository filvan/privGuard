import collections

from src.examples.program.traccar.model.baseModel import BaseModel
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.session.cache.cacheManager import CacheManager
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.order import Order
from src.examples.program.traccar.storage.query.request import Request

class PositionUtil:

    def __init__(self):
        pass

    def isLatest(cacheManager, position):
        lastPosition = cacheManager.getPosition(position.getDeviceId())
        return lastPosition is None or position.getFixTime().compareTo(lastPosition.getFixTime()) >= 0

    def calculateDistance(first, last, useOdometer):
        distance = 0
        firstOdometer = first.getDouble(Position.KEY_ODOMETER)
        lastOdometer = last.getDouble(Position.KEY_ODOMETER)

        if useOdometer and firstOdometer != 0.0 and lastOdometer != 0.0:
            distance = lastOdometer - firstOdometer
        else:
            distance = last.getDouble(Position.KEY_TOTAL_DISTANCE) - first.getDouble(Position.KEY_TOTAL_DISTANCE)
        return distance

    def getPositions(storage, deviceId, from_, to):
        return storage.getObjects(Position.__class__, Request(Columns.All(), Condition.And(Condition.Equals("deviceId", deviceId), Condition.Between("fixTime", "from", from_, "to", to)), Order("fixTime")))

    def getLatestPositions(storage, userId):
        devices = storage.getObjects(Device.__class__, Request(Columns.Include("id"), Condition.Permission(User.__class__, userId, Device.__class__)))
        deviceIds = devices.stream().map(BaseModel.getId()).collect(collections.toUnmodifiableSet())

        positions = storage.getObjects(Position.__class__, Request(Columns.All(), Condition.LatestPositions()))
        return positions.stream().filter(lambda position : deviceIds.contains(position.getDeviceId())).collect(collections.toList())
