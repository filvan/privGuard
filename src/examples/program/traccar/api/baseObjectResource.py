from kafka.protocol.api import Response

from src.examples.program.traccar.api.baseResource import BaseResource
from src.examples.program.traccar.helper.logAction import LogAction
from src.examples.program.traccar.model.baseModel import BaseModel
from src.examples.program.traccar.model.group import Group
from src.examples.program.traccar.model.permission import Permission
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.session.connectionManager import ConnectionManager
from src.examples.program.traccar.session.cache.cacheManager import CacheManager
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Equals
from src.examples.program.traccar.storage.query.request import Request


class BaseObjectResource(BaseResource):

    def __init__(self, baseClass):

        super().__init__()
        self.cache_manager = None
        self.connection_manager = None
        self.base_class = None

        self.base_class = baseClass

    def get_single(self, id):
        BaseResource.permissionsService.checkPermission(self.base_class, BaseResource.get_user_id(), id)
        entity = BaseResource.storage.getObject(self.base_class, Request(Columns.All(), Equals("id", id)))
        if entity is not None:
            return Response.ok(entity).build()
        else:
            return Response.status(Response.Status.NOT_FOUND).build()

    def add(self, entity):
        BaseResource.permissionsService.checkEdit(BaseResource.get_user_id(), entity, True)

        entity.setId(BaseResource.storage.addObject(entity, Request(Columns.Exclude("id"))))
        LogAction.create(BaseResource.get_user_id(), entity)
        BaseResource.storage.addPermission(
            Permission(User.__class__, BaseResource.get_user_id(), self.base_class, entity.getId()))
        self.cache_manager.invalidatePermission(True, User.__class__, BaseResource.get_user_id(), self.base_class,
                                                entity.getId())
        self.connection_manager.invalidatePermission(True, User.__class__, BaseResource.get_user_id(), self.base_class,
                                                     entity.getId())
        LogAction.link(BaseResource.get_user_id(), User.__class__, BaseResource.get_user_id(), self.base_class,
                       entity.getId())

        return Response.ok(entity).build()

    def update(self, entity):
        BaseResource.permissionsService.checkEdit(BaseResource.get_user_id(), entity, False)
        BaseResource.permissionsService.checkPermission(self.base_class, BaseResource.get_user_id(), entity.getId())

        if isinstance(entity, User):
            before = BaseResource.storage.getObject(User.__class__,
                                                    Request(Columns.All(), Equals("id", entity.getId())))
            BaseResource.permissionsService.checkUserUpdate(BaseResource.get_user_id(), before, entity)
        elif isinstance(entity, Group):
            group = entity
            if group.getId() == group.getGroupId():
                raise Exception("Cycle in group hierarchy")

        BaseResource.storage.updateObject(entity,
                                          Request(Columns.Exclude("id"), Equals("id", entity.getId())))
        if isinstance(entity, User):
            user = entity
            if user.getHashedPassword() is not None:
                BaseResource.storage.updateObject(entity, Request(Columns.Include("hashedPassword", "salt"),
                                                                  Equals("id", entity.getId())))
        self.cache_manager.updateOrInvalidate(True, entity)
        LogAction.edit(BaseResource.get_user_id(), entity)

        return Response.ok(entity).build()

    def remove(self, id):
        BaseResource.permissionsService.checkEdit(BaseResource.get_user_id(), self.base_class, False)
        BaseResource.permissionsService.checkPermission(self.base_class, BaseResource.get_user_id(), id)

        BaseResource.storage.removeObject(self.base_class, Request(Equals("id", id)))
        self.cache_manager.invalidate(self.base_class, id)

        LogAction.remove(BaseResource.get_user_id(), self.base_class, id)

        return Response.noContent().build()
