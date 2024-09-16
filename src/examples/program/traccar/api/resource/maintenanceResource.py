from src.examples.program.traccar.api.extendedObjectResource import ExtendedObjectResource
from src.examples.program.traccar.model.maintenance import Maintenance


class MaintenanceResource(ExtendedObjectResource):

    def __init__(self):
        super().__init__(Maintenance.__class__)
