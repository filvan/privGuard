class EventData:

    def __init__(self):
        self._event = None
        self._position = None
        self._device = None
        self._geofence = None
        self._maintenance = None



    def getEvent(self):
        return self._event

    def setEvent(self, event):
        self._event = event


    def getPosition(self):
        return self._position

    def setPosition(self, position):
        self._position = position


    def getDevice(self):
        return self._device

    def setDevice(self, device):
        self._device = device


    def getGeofence(self):
        return self._geofence

    def setGeofence(self, geofence):
        self._geofence = geofence


    def getMaintenance(self):
        return self._maintenance

    def setMaintenance(self, maintenance):
        self._maintenance = maintenance
