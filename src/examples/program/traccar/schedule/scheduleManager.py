from src.examples.program.traccar.lifecycleObject import LifecycleObject
from src.examples.program.traccar.schedule.taskDeviceInactivityCheck import TaskDeviceInactivityCheck
from src.examples.program.traccar.schedule.taskHealthCheck import TaskHealthCheck
from src.examples.program.traccar.schedule.taskReports import TaskReports
from src.examples.program.traccar.schedule.taskWebSocketKeepalive import TaskWebSocketKeepalive


class ScheduleManager(LifecycleObject):


    def __init__(self, injector):

        self._injector = None
        self._executor = None

        self._injector = injector

    def start(self):
        self._executor = "Executors.newSingleThreadScheduledExecutor()"
        tasks = list(TaskReports.__class__, TaskDeviceInactivityCheck.__class__, TaskWebSocketKeepalive.__class__, TaskHealthCheck.__class__)
        tasks.forEach(lambda task : self._injector.getInstance(task).schedule(self._executor))

    def stop(self):
        if self._executor is not None:
            self._executor.shutdown()
            self._executor = None
