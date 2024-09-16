from kafka.protocol.api import Response

from src.examples.program.traccar.api.extendedObjectResource import ExtendedObjectResource
from src.examples.program.traccar.model.attribute import Attribute
from src.examples.program.traccar.handler.computedAttributesHandler import ComputedAttributesHandler
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition, LatestPositions
from src.examples.program.traccar.storage.query.request import Request


class AttributeResource(ExtendedObjectResource):
    def __init__(self):
        super().__init__(Attribute)
        self.computedAttributesHandler = ComputedAttributesHandler()

    def post(self, request, device_id: int, entity: Attribute):
        if request.path.endswith('/test'):
            return self.test(device_id, entity)
        else:
            return self.add()

    def test(self, device_id, entity: Attribute):
        self.permissions_service.check_admin(self.get_user_id())
        self.permissions_service.check_permission(Device, self.get_user_id(), device_id)

        position = self.storage.get_object(Position, Request(
            Columns.All(),
            LatestPositions(device_id)
        ))

        result = self.computedAttributesHandler.compute_attribute(entity, position)
        if result is not None:
            if entity.getType() == "number" or entity.getType() == "boolean":
                return Response.ok(result).build()
            else:
                return Response.ok(result.__str__()).build()
        else:
            return Response.noContent().build()

    def add(self, entity: Attribute):
        self.permissions_service.check_admin(self.get_user_id())
        return super().add(entity)

    def update(self, entity: Attribute):
        self.permissions_service.check_admin(self.get_user_id())
        return super().update(entity)

    def remove(self, id):
        self.permissions_service.check_admin(self.get_user_id())
        # Implement the remove logic here
        return super().remove(id)