import sys


class Disableable:

    def getDisabled(self):
        pass

    def setDisabled(self, disabled):
        pass

    def getExpirationTime(self):
        pass

    def setExpirationTime(self, expirationTime):
        pass

    def checkDisabled(self):
        if self.getDisabled():
            raise RuntimeError(self.__class__.__name__ + " is disabled")
        if self.getExpirationTime() is not None and sys.currentTimeMillis() > self.getExpirationTime().getTime():
            raise RuntimeError(self.__class__.__name__ + " has expired")
