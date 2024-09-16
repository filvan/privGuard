import datetime

from kafka.protocol.api import Response
from numpy import array

from src.examples.program.traccar.api.baseResource import BaseResource
from src.examples.program.traccar.database.openIdProvider import OpenIdProvider
from src.examples.program.traccar.helper.model.userUtil import UserUtil
from src.examples.program.traccar.mail.mailManager import MailManager
from src.examples.program.traccar.geocoder.geocoder import Geocoder
from src.examples.program.traccar.helper.log import Log
from src.examples.program.traccar.helper.logAction import LogAction
from src.examples.program.traccar.model.server import Server
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.session.cache.cacheManager import CacheManager
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class ServerResource(BaseResource):

    def __init__(self):

        self._cacheManager = None
        self._mailManager = None
        self._openIdProvider = None
        self._geocoder = None






    def get(self):
        server = self.storage.getObject(Server.__class__, Request(Columns.All()))
        server.setEmailEnabled(self._mailManager.getEmailEnabled())
        server.setGeocoderEnabled(self._geocoder is not None)
        server.setOpenIdEnabled(self._openIdProvider is not None)
        server.setOpenIdForce(self._openIdProvider is not None and self._openIdProvider.getForce())
        user = self.permissions_service.getUser(self.get_user_id())
        if user is not None:
            if user.getAdministrator():
                server.setStorageSpace(Log.getStorageSpace())
        else:
            server.setNewServer(UserUtil.isEmpty(self.storage))
        if user is not None and user.getAdministrator():
            server.setStorageSpace(Log.getStorageSpace())
        return server

    def update(self, entity):
        self.permissions_service.checkAdmin(self.get_user_id())
        self.storage.updateObject(entity, Request(Columns.Exclude("id"), Condition.Equals("id", entity.getId())))
        self._cacheManager.updateOrInvalidate(True, entity)
        LogAction.edit(self.get_user_id(), entity)
        return Response.ok(entity).build()

    def geocode(self, latitude, longitude):
        if self._geocoder is not None:
            return self._geocoder.getAddress(latitude, longitude, None)
        else:
            raise Exception("Reverse geocoding is not enabled")

    def timezones(self):
        return array(datetime.tzinfo.getAvailableIDs())
