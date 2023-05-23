import collections

from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.handler.events.baseEventHandler import BaseEventHandler
from src.examples.program.traccar.helper.model.attributeUtil import AttributeUtil
from src.examples.program.traccar.helper.model.positionUtil import PositionUtil
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.reports.common.tripsConfig import TripsConfig
from src.examples.program.traccar.session.cache.cacheManager import CacheManager
from src.examples.program.traccar.session.state.motionState import MotionState
from src.examples.program.traccar.session.state.motionProcessor import MotionProcessor
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class MotionEventHandler(BaseEventHandler):

    _LOGGER = "LoggerFactory.getLogger(MotionEventHandler.class)"


    def __init__(self, cacheManager, storage):

        self._cacheManager = None
        self._storage = None

        self._cacheManager = cacheManager
        self._storage = storage

    def analyzePosition(self, position):

        deviceId = position.getDeviceId()
        device = self._cacheManager.getObject(Device.__class__, deviceId)
        if device is None or not PositionUtil.isLatest(self._cacheManager, position):
            return None
        processInvalid = AttributeUtil.lookup(self._cacheManager, Keys.EVENT_MOTION_PROCESS_INVALID_POSITIONS, deviceId)
        if (not processInvalid) and not position.getValid():
            return None

        tripsConfig = TripsConfig(AttributeUtil.CacheProvider(self._cacheManager, deviceId))
        state = MotionState.fromDevice(device)
        MotionProcessor.updateState(state, position, position.getBoolean(Position.KEY_MOTION), tripsConfig)
        if state.isChanged():
            state.toDevice(device)
            try:
                self._storage.updateObject(device, Request(Columns.Include("motionStreak", "motionState", "motionTime", "motionDistance"), Condition.Equals("id", device.getId())))
            except StorageException as e:
                MotionEventHandler._LOGGER.warn("Update device motion error", e)
        return collections.singletonMap(state.getEvent(), position) if state.getEvent() is not None else None
