import sys
from multiprocessing.sharedctypes import synchronized

from kafka.metrics.stats.rate import TimeUnit

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class DeviceLookupService:

    _LOGGER = "LoggerFactory.getLogger(DeviceLookupService.class)"

    _INFO_TIMEOUT_MS = TimeUnit.MINUTES.toMillis(60)
    _THROTTLE_MIN_MS = TimeUnit.MINUTES.toMillis(1)
    _THROTTLE_MAX_MS = TimeUnit.MINUTES.toMillis(30)



    class IdentifierInfo:

        def __init__(self):
            self._lastQuery = 0
            self._delay = 0
            self._timeout = None


    class IdentifierTask():


        def __init__(self, outerInstance, uniqueId):

            self._uniqueId = None

            self._outerInstance = outerInstance

            self._uniqueId = uniqueId

        def run(self, timeout):
            DeviceLookupService._LOGGER.debug("Device lookup expired {}", self._uniqueId)
            synchronized(self._outerInstance)
            self._outerInstance._identifierMap.pop(self._uniqueId)


    def __init__(self, config, storage, timer):

        self._storage = None
        self._timer = None
        self._throttlingEnabled = False
        self._identifierMap = {}

        self._storage = storage
        self._timer = timer
        self._throttlingEnabled = config.getBoolean(Keys.DATABASE_THROTTLE_UNKNOWN)

    def _isThrottled(self, uniqueId):
        if self._throttlingEnabled:
            info = self._identifierMap[uniqueId]
            return info is not None and sys.currentTimeMillis() < info.lastQuery + info.delay
        else:
            return False

    def _lookupSucceeded(self, uniqueId):
        if self._throttlingEnabled:
            info = self._identifierMap.pop(uniqueId)
            if info is not None:
                info.timeout.cancel()

    def _lookupFailed(self, uniqueId):
        if self._throttlingEnabled:
            info = self._identifierMap[uniqueId]
            if info is not None:
                info.timeout.cancel()
                info.delay = min(info.delay * 2, DeviceLookupService._THROTTLE_MAX_MS)
            else:
                info = self.IdentifierInfo()
                self._identifierMap[uniqueId] = info
                info.delay = DeviceLookupService._THROTTLE_MIN_MS
            info.lastQuery = sys.currentTimeMillis()
            info.timeout = self._timer.newTimeout(self.IdentifierTask(self, uniqueId), DeviceLookupService._INFO_TIMEOUT_MS, TimeUnit.MILLISECONDS)
            DeviceLookupService._LOGGER.debug("Device lookup {} throttled for {} ms", uniqueId, info.delay)

    def lookup(self, uniqueIds):
        device = None
        try:
            for uniqueId in uniqueIds:
                if not self._isThrottled(uniqueId):
                    device = self._storage.getObject(Device.__class__, Request(Columns.All(), Condition.Equals("uniqueId", uniqueId)))
                    if device is not None:
                        self._lookupSucceeded(uniqueId)
                        break
                    else:
                        self._lookupFailed(uniqueId)
                else:
                    DeviceLookupService._LOGGER.debug("Device lookup throttled {}", uniqueId)
        except StorageException as e:
            DeviceLookupService._LOGGER.warn("Find device error", e)
        return device

