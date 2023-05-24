from kafka.protocol.api import Response

from src.examples.program.traccar.api.baseResource import BaseResource
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class EventResource(BaseResource):
    def get(self, id):
        event = self.storage.getObject(Event.__class__, Request(Columns.All(), Condition.Equals("id", id)))
        if event is None:
            raise Exception(Response.status(Response.Status.NOT_FOUND).build())
        self.permissionsService.checkPermission(Device.__class__, self.getUserId(), event.getDeviceId())
        return event
