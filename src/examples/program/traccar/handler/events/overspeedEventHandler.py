import collections

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.handler.events.baseEventHandler import BaseEventHandler
from src.examples.program.traccar.helper.model.attributeUtil import AttributeUtil
from src.examples.program.traccar.helper.model.positionUtil import PositionUtil
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.geofence import Geofence
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.cache.cacheManager import CacheManager
from src.examples.program.traccar.session.state.overspeedProcessor import OverspeedProcessor
from src.examples.program.traccar.session.state.overspeedState import OverspeedState
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class OverspeedEventHandler(BaseEventHandler):

    _LOGGER = "LoggerFactory.getLogger(OverspeedEventHandler.class)"



    def __init__(self, config, cacheManager, storage):

        self._cacheManager = None
        self._storage = None
        self._minimalDuration = 0
        self._preferLowest = False

        self._cacheManager = cacheManager
        self._storage = storage
        self._minimalDuration = config.getLong(Keys.EVENT_OVERSPEED_MINIMAL_DURATION) * 1000
        self._preferLowest = config.getBoolean(Keys.EVENT_OVERSPEED_PREFER_LOWEST)

    def analyzePosition(self, position):

        deviceId = position.getDeviceId()
        device = self._cacheManager.getObject(Device.__class__, position.getDeviceId())
        if device is None:
            return None
        if (not PositionUtil.isLatest(self._cacheManager, position)) or not position.getValid():
            return None

        speedLimit = AttributeUtil.lookup(self._cacheManager, Keys.EVENT_OVERSPEED_LIMIT, deviceId)

        positionSpeedLimit = position.getDouble(Position.KEY_SPEED_LIMIT)
        if positionSpeedLimit > 0:
            speedLimit = positionSpeedLimit

        geofenceSpeedLimit = 0
        overspeedGeofenceId = 0

        if position.getGeofenceIds() is not None:
            for geofenceId in position.getGeofenceIds():
                geofence = self._cacheManager.getObject(Geofence.__class__, geofenceId)
                if geofence is not None:
                    currentSpeedLimit = geofence.getDouble(Keys.EVENT_OVERSPEED_LIMIT.getKey())
                    if currentSpeedLimit > 0 and geofenceSpeedLimit == 0 or self._preferLowest and currentSpeedLimit < geofenceSpeedLimit or (not self._preferLowest) and currentSpeedLimit > geofenceSpeedLimit:
                        geofenceSpeedLimit = currentSpeedLimit
                        overspeedGeofenceId = geofenceId
        if geofenceSpeedLimit > 0:
            speedLimit = geofenceSpeedLimit

        if speedLimit == 0:
            return None

        state = OverspeedState.fromDevice(device)
        OverspeedProcessor.updateState(state, position, speedLimit, self._minimalDuration, overspeedGeofenceId)
        if state.isChanged():
            state.toDevice(device)
            try:
                self._storage.updateObject(device, Request(Columns.Include("overspeedState", "overspeedTime", "overspeedGeofenceId"), Condition.Equals("id", device.getId())))
            except StorageException as e:
                OverspeedEventHandler._LOGGER.warn("Update device overspeed error", e)
        return collections.singletonMap(state.getEvent(), position) if state.getEvent() is not None else None
