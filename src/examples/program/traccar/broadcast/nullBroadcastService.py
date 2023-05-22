from .broadcastService import BroadcastService


class NullBroadcastService(BroadcastService):

    def singleInstance(self):
        return True

    def registerListener(self, listener):
        pass



    def start(self):
        pass



    def stop(self):
        pass
