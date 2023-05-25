import sys

from kafka.metrics.stats.rate import TimeUnit
from setuptools.extension import Library

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys

import math

from src.examples.program.traccar.schedule.scheduleTask import ScheduleTask


class TaskHealthCheck(ScheduleTask):

    _LOGGER = "LoggerFactory.getLogger(TaskHealthCheck.class)"




    def __init__(self, config, client):

        self._config = None
        self._client = None
        self._systemD = None
        self._enabled = False
        self._period = 0

        self._config = config
        self._client = client
        if (not config.getBoolean(Keys.WEB_DISABLE_HEALTH_CHECK)) and sys.getProperty("os.name").toLowerCase().startsWith("linux"):
            try:
                self._systemD = "Native.load(\"systemd\", SystemD.class)"
                watchdogTimer = sys.getenv("WATCHDOG_USEC")
                if watchdogTimer is not None and watchdogTimer:
                    self._period = math.trunc(int(watchdogTimer) / float(math.trunc(1000 * 4 / float(5))))
                if self._period > 0:
                    TaskHealthCheck._LOGGER.info("Health check enabled with period {}", self._period)
                    self._enabled = True
            except Exception as e:
                TaskHealthCheck._LOGGER.warn("No systemd support", e)

    def _getUrl(self):
        address = self._config.getString(Keys.WEB_ADDRESS, "localhost")
        port = self._config.getInteger(Keys.WEB_PORT)
        return "http://" + address + ":" + str(port) + "/api/server"

    def schedule(self, executor):
        if self._enabled:
            executor.scheduleAtFixedRate(self, self._period, self._period, TimeUnit.MILLISECONDS)

    def run(self):
        TaskHealthCheck._LOGGER.debug("Health check running")
        status = self._client.target(self._getUrl()).request().get().getStatus()
        if status == 200:
            result = self._systemD.sd_notify(0, "WATCHDOG=1")
            if result < 0:
                TaskHealthCheck._LOGGER.warn("Health check notify error {}", result)
        else:
            TaskHealthCheck._LOGGER.warn("Health check failed with status {}", status)

    class SystemD(Library):
        def sd_notify(self, unset_environment, state):
            pass
