class Endpoint:


    def __init__(self, channel, remoteAddress):
        self._channel = None
        self._remoteAddress = None

        self._channel = channel
        self._remoteAddress = remoteAddress

    def getChannel(self):
        return self._channel

    def getRemoteAddress(self):
        return self._remoteAddress

    def equals(self, o):
        if self is o:
            return True
        if o is None or self.__class__ != type(o):
            return False
        endpoint = o
        return self._channel is endpoint._channel and self._remoteAddress is endpoint._remoteAddress

