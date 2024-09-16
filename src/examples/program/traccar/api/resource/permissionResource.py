import collections

from kafka.protocol.api import Response

from src.examples.program.traccar.api.baseResource import BaseResource
from src.examples.program.traccar.helper.logAction import LogAction
from src.examples.program.traccar.model.permission import Permission
from src.examples.program.traccar.model.userRestriction import UserRestrictions
from src.examples.program.traccar.session.cache.cacheManager import CacheManager
from src.examples.program.traccar.storage.storageException import StorageException

class PermissionsResource(BaseResource):

    def __init__(self):

        self._cacheManager = None



    def _checkPermission(self, permission):
        if self.permissions_service.notAdmin(self.get_user_id()):
            self.permissions_service.checkPermission(permission.getOwnerClass(), self.get_user_id(), permission.getOwnerId())
            self.permissions_service.checkPermission(permission.getPropertyClass(), self.get_user_id(), permission.getPropertyId())

    def _checkPermissionTypes(self, entities):
        keys = None
        for entity in entities:
            if keys is not None & entity.keySet() is not keys:
                raise Exception(Response.status(Response.Status.BAD_REQUEST).build())
            keys = entity.keySet()

    def add(self, entities):
        self.permissions_service.checkRestriction(self.get_user_id(), UserRestrictions.getReadonly())
        self._checkPermissionTypes(entities)
        for entity in entities:
            permission = Permission(entity)
            self._checkPermission(permission)
            self.storage.addPermission(permission)
            self._cacheManager.invalidatePermission(True, permission.getOwnerClass(), permission.getOwnerId(), permission.getPropertyClass(), permission.getPropertyId())
            LogAction.link(self.get_user_id(), permission.getOwnerClass(), permission.getOwnerId(), permission.getPropertyClass(), permission.getPropertyId())
        return Response.noContent().build()

    def add(self, entity):
        return self.add(collections.singletonList(entity))

    def remove(self, entities):
        self.permissions_service.checkRestriction(self.get_user_id(), UserRestrictions.getReadonly())
        self._checkPermissionTypes(entities)
        for entity in entities:
            permission = Permission(entity)
            self._checkPermission(permission)
            self.storage.removePermission(permission)
            self._cacheManager.invalidatePermission(True, permission.getOwnerClass(), permission.getOwnerId(), permission.getPropertyClass(), permission.getPropertyId())
            LogAction.unlink(self.get_user_id(), permission.getOwnerClass(), permission.getOwnerId(), permission.getPropertyClass(), permission.getPropertyId())
        return Response.noContent().build()

    def remove(self, entity):
        return self.remove(collections.singletonList(entity))
