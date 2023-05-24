class DeviceReportSection:

    def __init__(self):
        self._deviceName = None
        self._groupName = ""
        self._objects = None



    def getDeviceName(self):
        return self._deviceName

    def setDeviceName(self, deviceName):
        self._deviceName = deviceName


    def getGroupName(self):
        return self._groupName

    def setGroupName(self, groupName):
        self._groupName = groupName


    def getObjects(self):
        return self._objects

    def setObjects(self, objects):
        self._objects = list(objects)
