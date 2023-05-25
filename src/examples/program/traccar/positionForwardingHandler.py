from kafka.metrics.stats.rate import TimeUnit
from kafka.producer.record_accumulator import AtomicInteger

from src.examples.program.traccar.baseDataHandler import BaseDataHandler
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.forward.positionData import PositionData
from src.examples.program.traccar.forward.positionForwarder import PositionForwarder
from src.examples.program.traccar.forward.resultHandler import ResultHandler
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.session.cache.cacheManager import CacheManager

class PositionForwardingHandler(BaseDataHandler):

    _LOGGER = "LoggerFactory.getLogger(PositionForwardingHandler.__class__)"
    def __init__(self, config, cacheManager, timer, positionForwarder):

        self._cacheManager = None
        self._timer = None
        self._positionForwarder = None
        self._retryEnabled = False
        self._retryDelay = 0
        self._retryCount = 0
        self._retryLimit = 0
        self._deliveryPending = None


        self._cacheManager = cacheManager
        self._timer = timer
        self._positionForwarder = positionForwarder

        self._retryEnabled = config.getBoolean(Keys.FORWARD_RETRY_ENABLE)
        self._retryDelay = config.getInteger(Keys.FORWARD_RETRY_DELAY)
        self._retryCount = config.getInteger(Keys.FORWARD_RETRY_COUNT)
        self._retryLimit = config.getInteger(Keys.FORWARD_RETRY_LIMIT)

        self._deliveryPending = AtomicInteger()

    class AsyncRequestAndCallback(ResultHandler, "TimerTask"):




        def __init__(self, positionData):

            self._positionData = None
            self._retries = 0

            self._self = self

            self._positionData = positionData
            self._deliveryPending.incrementAndGet()

        def _send(self):
            PositionForwardingHandler.forward(self._positionData, self)

        def _retry(self, throwable):
            scheduled = False
            try:
                if self._retryEnabled and self._deliveryPending.get() <= self._retryLimit and self._retries < self._retryCount:
                    self._schedule()
                    scheduled = True
            finally:
                pending = self._deliveryPending.get() if scheduled else self._deliveryPending.decrementAndGet()
                PositionForwardingHandler._LOGGER.warn("Position forwarding failed: " + str(pending) + " pending", throwable)

        def _schedule(self):
            self._timer.newTimeout(self, self._retryDelay * int(2) ** self._retries, TimeUnit.MILLISECONDS)
            self._retries += 1

        def onResult(self, success, throwable):
            if success:
                self._deliveryPending.decrementAndGet()
            else:
                self._retry(throwable)

        def run(self, timeout):
            sent = False
            try:
                if not timeout.isCancelled():
                    self._send()
                    sent = True
            finally:
                if not sent:
                    self._deliveryPending.decrementAndGet()

    def handlePosition(self, position):
        if self._positionForwarder is not None:
            positionData = PositionData()
            positionData.setPosition(position)
            positionData.setDevice(self._cacheManager.getObject(Device.__class__, position.getDeviceId()))
            (self.AsyncRequestAndCallback(self, positionData)).send()
        return position
