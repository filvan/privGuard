from .extendedModel import ExtendedModel
from src.examples.program.traccar.storage.storageName import StorageName


class Statistics(ExtendedModel):

    def __init__(self):
        super().__init__()
        self._captureTime = None
        self._activeUsers = 0
        self._activeDevices = 0
        self._requests = 0
        self._messagesReceived = 0
        self._messagesStored = 0
        self._mailSent = 0
        self._smsSent = 0
        self._geocoderRequests = 0
        self._geolocationRequests = 0
        self._protocols = None

    def getCaptureTime(self):
        return self._captureTime

    def setCaptureTime(self, captureTime):
        self._captureTime = captureTime

    def getActiveUsers(self):
        return self._activeUsers

    def setActiveUsers(self, activeUsers):
        self._activeUsers = activeUsers

    def getActiveDevices(self):
        return self._activeDevices

    def setActiveDevices(self, activeDevices):
        self._activeDevices = activeDevices

    def getRequests(self):
        return self._requests

    def setRequests(self, requests):
        self._requests = requests

    def getMessagesReceived(self):
        return self._messagesReceived

    def setMessagesReceived(self, messagesReceived):
        self._messagesReceived = messagesReceived

    def getMessagesStored(self):
        return self._messagesStored

    def setMessagesStored(self, messagesStored):
        self._messagesStored = messagesStored

    def getMailSent(self):
        return self._mailSent

    def setMailSent(self, mailSent):
        self._mailSent = mailSent

    def getSmsSent(self):
        return self._smsSent

    def setSmsSent(self, smsSent):
        self._smsSent = smsSent

    def getGeocoderRequests(self):
        return self._geocoderRequests

    def setGeocoderRequests(self, geocoderRequests):
        self._geocoderRequests = geocoderRequests

    def getGeolocationRequests(self):
        return self._geolocationRequests

    def setGeolocationRequests(self, geolocationRequests):
        self._geolocationRequests = geolocationRequests

    def getProtocols(self):
        return self._protocols

    def setProtocols(self, protocols):
        self._protocols = protocols
