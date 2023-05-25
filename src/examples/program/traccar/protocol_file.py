class Protocol:

    def getName(self):
        pass

    def getConnectorList(self):
        pass

    def getSupportedDataCommands(self):
        pass

    def sendDataCommand(self, channel, remoteAddress, command):
        pass

    def getSupportedTextCommands(self):
        pass

    def sendTextCommand(self, destAddress, command):
        pass
