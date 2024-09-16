from kafka.protocol.api import Response

from src.examples.program.traccar.api.baseResource import BaseResource
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Equals
from src.examples.program.traccar.storage.query.request import Request


class EventResource(BaseResource):
    def get(self, id):
        event = self.storage.getObject(Event.__class__, Request(Columns.All(), Equals("id", id)))
        if event is None:
            raise Exception(Response.status(Response.Status.NOT_FOUND).build())
        self.permissions_service.checkPermission(Device.__class__, self.get_user_id(), event.getDeviceId())
        return event
