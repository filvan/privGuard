from src.examples.program.traccar.api.extendedObjectResource import ExtendedObjectResource
from src.examples.program.traccar.model.driver import Driver

class DriverResource(ExtendedObjectResource):

    def __init__(self):
        super().__init__(Driver.__class__)
