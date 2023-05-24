from src.examples.program.traccar.api.simpleObjectResource import SimpleObjectResource
from src.examples.program.traccar.model.group import Group

class GroupResource(SimpleObjectResource):

    def __init__(self):
        super().__init__(Group.__class__)
