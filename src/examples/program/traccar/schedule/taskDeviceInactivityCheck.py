import sys

from kafka.metrics.stats.rate import TimeUnit

from src.examples.program.traccar.database.notificationManager import NotificationManager
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.schedule.scheduleTask import ScheduleTask
from src.examples.program.traccar.storage.query.request import Request
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns

import math

class TaskDeviceInactivityCheck(ScheduleTask):

    _LOGGER = "LoggerFactory.getLogger(TaskDeviceInactivityCheck.class)"

    ATTRIBUTE_DEVICE_INACTIVITY_START = "deviceInactivityStart"
    ATTRIBUTE_DEVICE_INACTIVITY_PERIOD = "deviceInactivityPeriod"
    ATTRIBUTE_LAST_UPDATE = "lastUpdate"

    _CHECK_PERIOD_MINUTES = 15


    def __init__(self, storage, notificationManager):

        self._storage = None
        self._notificationManager = None

        self._storage = storage
        self._notificationManager = notificationManager

    def schedule(self, executor):
        executor.scheduleAtFixedRate(self, TaskDeviceInactivityCheck._CHECK_PERIOD_MINUTES, TaskDeviceInactivityCheck._CHECK_PERIOD_MINUTES, TimeUnit.MINUTES)

    def run(self):
        currentTime = sys.currentTimeMillis()
        checkPeriod = TimeUnit.MINUTES.toMillis(TaskDeviceInactivityCheck._CHECK_PERIOD_MINUTES)

        events = {}

        try:
            for device in self._storage.getObjects(Device.__class__, Request(Columns.All())):
                if device.getLastUpdate() is not None and self._checkDevice(device, currentTime, checkPeriod):
                    event = Event(Event.TYPE_DEVICE_INACTIVE, device.getId())
                    event.set(TaskDeviceInactivityCheck.ATTRIBUTE_LAST_UPDATE, device.getLastUpdate().getTime())
                    events[event] = None
        except StorageException as e:
            TaskDeviceInactivityCheck._LOGGER.warn("Get devices error", e)

        self._notificationManager.updateEvents(events)

    def _checkDevice(self, device, currentTime, checkPeriod):
        deviceInactivityStart = device.getLong(TaskDeviceInactivityCheck.ATTRIBUTE_DEVICE_INACTIVITY_START)
        if deviceInactivityStart > 0:
            timeThreshold = device.getLastUpdate().getTime() + deviceInactivityStart
            if currentTime >= timeThreshold:

                if currentTime - checkPeriod < timeThreshold:
                    return True

                deviceInactivityPeriod = device.getLong(TaskDeviceInactivityCheck.ATTRIBUTE_DEVICE_INACTIVITY_PERIOD)
                if deviceInactivityPeriod > 0:
                    count = math.trunc((currentTime - timeThreshold - 1) / float(deviceInactivityPeriod))
                    timeThreshold += count * deviceInactivityPeriod
                    return currentTime - checkPeriod < timeThreshold

        return False
