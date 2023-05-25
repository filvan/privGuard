from src.examples.program.traccar.schedule.scheduleTask import ScheduleTask
from src.examples.program.traccar.session.connectionManager import ConnectionManager

class TaskWebSocketKeepalive(ScheduleTask):

    _PERIOD_SECONDS = 55


    def __init__(self, connectionManager):

        self._connectionManager = None

        self._connectionManager = connectionManager

    def schedule(self, executor):
        executor.scheduleAtFixedRate(self, TaskWebSocketKeepalive._PERIOD_SECONDS, TaskWebSocketKeepalive._PERIOD_SECONDS, TimeUnit.SECONDS)

    def run(self):
        self._connectionManager.sendKeepalive()
