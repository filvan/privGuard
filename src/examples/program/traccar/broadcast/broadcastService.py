from src.examples.program.traccar.lifecycleObject import LifecycleObject
from .broadcastInterface import BroadcastInterface
class BroadcastService(LifecycleObject, BroadcastInterface):
    def singleInstance(self):
        pass
    def registerListener(self, listener):
        pass
