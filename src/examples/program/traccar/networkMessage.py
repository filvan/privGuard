class NetworkMessage:


    def __init__(self, message, remoteAddress):
        self._remoteAddress = None
        self._message = None

        self._message = message
        self._remoteAddress = remoteAddress

    def getRemoteAddress(self):
        return self._remoteAddress

    def getMessage(self):
        return self._message
