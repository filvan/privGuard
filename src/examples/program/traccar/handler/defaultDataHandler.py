from src.examples.program.traccar.baseDataHandler import BaseDataHandler
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.request import Request

class DefaultDataHandler(BaseDataHandler):

    _LOGGER =" LoggerFactory.getLogger(DefaultDataHandler.class)"


    def __init__(self, storage):

        self._storage = None

        self._storage = storage

    def handlePosition(self, position):

        try:
            position.setId(self._storage.addObject(position, Request(Columns.Exclude("id"))))
        except Exception as error:
            DefaultDataHandler._LOGGER.warn("Failed to store position", error)

        return position
