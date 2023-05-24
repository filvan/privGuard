import calendar
from tkinter.tix import Form

from numpy import array
from wrapt import synchronized

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.helper.dateUtil import DateUtil
from src.examples.program.traccar.model.statistics import Statistics
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.request import Request

import datetime

class StatisticsManager:

    _LOGGER = "LoggerFactory.getLogger(StatisticsManager.class)"

    _SPLIT_MODE = calendar.DAY_OF_MONTH





    def __init__(self, config, storage, client, objectMapper):

        self._config = None
        self._storage = None
        self._client = None
        self._objectMapper = None
        self._lastUpdate = int(datetime.datetime().get(StatisticsManager._SPLIT_MODE))
        self._users = array()
        self._deviceProtocols = {}
        self._requests = 0
        self._messagesReceived = 0
        self._messagesStored = 0
        self._mailSent = 0
        self._smsSent = 0
        self._geocoderRequests = 0
        self._geolocationRequests = 0

        self._config = config
        self._storage = storage
        self._client = client
        self._objectMapper = objectMapper

    def _checkSplit(self):
        currentUpdate = datetime.datetime().get(StatisticsManager._SPLIT_MODE)
        if self._lastUpdate.getAndSet(currentUpdate) != currentUpdate:
            statistics = Statistics()

            statistics.setCaptureTime(datetime.date())
            statistics.setActiveUsers(self._users.size())
            statistics.setActiveDevices(len(self._deviceProtocols))
            statistics.setRequests(self._requests)
            statistics.setMessagesReceived(self._messagesReceived)
            statistics.setMessagesStored(self._messagesStored)
            statistics.setMailSent(self._mailSent)
            statistics.setSmsSent(self._smsSent)
            statistics.setGeocoderRequests(self._geocoderRequests)
            statistics.setGeolocationRequests(self._geolocationRequests)
            if self._deviceProtocols:
                protocols = {}
                for protocol in self._deviceProtocols.values():
                     count = 0
                     "protocols.compute(protocol,count + 1 if var = lambda key, count: count is not None else 1)"
            statistics.setProtocols(protocols)

            self._users.clear()
            self._deviceProtocols.clear()
            self._requests = 0
            self._messagesReceived = 0
            self._messagesStored = 0
            self._mailSent = 0
            self._smsSent = 0
            self._geocoderRequests = 0
            self._geolocationRequests = 0

            try:
                self._storage.addObject(statistics, Request(Columns.Exclude("id")))
            except StorageException as e:
                StatisticsManager._LOGGER.warn("Error saving statistics", e)

            url = self._config.getString(Keys.SERVER_STATISTICS)
            if url is not None:
                time = DateUtil.formatDate(statistics.getCaptureTime())

                form = Form()
                form.param("version", self.__class__.getPackage().getImplementationVersion())
                form.param("captureTime", time)
                form.param("activeUsers", str(statistics.getActiveUsers()))
                form.param("activeDevices", str(statistics.getActiveDevices()))
                form.param("requests", str(statistics.getRequests()))
                form.param("messagesReceived", str(statistics.getMessagesReceived()))
                form.param("messagesStored", str(statistics.getMessagesStored()))
                form.param("mailSent", str(statistics.getMailSent()))
                form.param("smsSent", str(statistics.getSmsSent()))
                form.param("geocoderRequests", str(statistics.getGeocoderRequests()))
                form.param("geolocationRequests", str(statistics.getGeolocationRequests()))
                if statistics.getProtocols() is not None:
                    try:
                        form.param("protocols", self._objectMapper.writeValueAsString(statistics.getProtocols()))
                    except Exception as e:
                        StatisticsManager._LOGGER.warn("Failed to serialize protocols", e)

                self._client.target(url).request().async_().post("Entity.form(form)")

    def registerRequest(self, userId):
        self._checkSplit()
        self._requests += 1
        if userId != 0:
            self._users.add(userId)

    def registerMessageReceived(self):
        self._checkSplit()
        self._messagesReceived += 1

    def registerMessageStored(self, deviceId, protocol):
        self._checkSplit()
        self._messagesStored += 1
        if deviceId != 0:
            self._deviceProtocols[deviceId] = protocol

    def registerMail(self):
        self._checkSplit()
        self._mailSent += 1

    def registerSms(self):
        self._checkSplit()
        self._smsSent += 1

    def registerGeocoderRequest(self):
        self._checkSplit()
        self._geocoderRequests += 1

    def registerGeolocationRequest(self):
        self._checkSplit()
        self._geocoderRequests += 1
