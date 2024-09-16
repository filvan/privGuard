from src.examples.program.traccar.api.simpleObjectResource import SimpleObjectResource
from src.examples.program.traccar.model.calendar import Calendar


class CalendarResource(SimpleObjectResource):

    def __init__(self):
        super().__init__(Calendar.__class__)
