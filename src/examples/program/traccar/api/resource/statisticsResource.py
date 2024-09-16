from src.examples.program.traccar.api.baseResource import BaseResource
from src.examples.program.traccar.model.statistics import Statistics
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.order import Order
from src.examples.program.traccar.storage.query.request import Request


class StatisticsResource(BaseResource):

    def get(self, from_, to):
        self.permissions_service.checkAdmin(self.get_user_id())
        return self.storage.getObjects(Statistics.__class__, Request(Columns.All(), Condition.Between("captureTime", "from", from_, "to", to), Order("captureTime")))
