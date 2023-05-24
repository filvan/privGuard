from src.examples.program.traccar.api.simpleObjectResource import SimpleObjectResource
from src.examples.program.traccar.model.order import Order

class OrderResource(SimpleObjectResource):

    def __init__(self):
        super().__init__(Order.__class__)
