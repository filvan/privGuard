import json
import logging
from collections import defaultdict
from src.examples.program.traccar.helper.model.positionUtil import PositionUtil
from src.examples.program.traccar.session.connectionManager import ConnectionManager
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.storage import Storage


class AsyncSocket(ConnectionManager.UpdateListener):
    LOGGER = logging.getLogger(__name__)

    KEY_DEVICES = "devices"
    KEY_POSITIONS = "positions"
    KEY_EVENTS = "events"
    KEY_LOGS = "logs"

    def __init__(self, object_mapper, connection_manager, storage, user_id):
        self.object_mapper = object_mapper
        self.connection_manager = connection_manager
        self.storage = storage
        self.user_id = user_id
        self.include_logs = False

    def on_websocket_connect(self, session):
        super().on_websocket_connect(session)

        try:
            data = {
                self.KEY_POSITIONS: PositionUtil.get_latest_positions(self.storage, self.user_id)
            }
            self.send_data(data)
            self.connection_manager.add_listener(self.user_id, self)
        except StorageException as e:
            raise RuntimeError(e)

    def on_websocket_close(self, status_code, reason):
        super().on_websocket_close(status_code, reason)
        self.connection_manager.remove_listener(self.user_id, self)

    def on_websocket_text(self, message):
        super().on_websocket_text(message)

        try:
            self.include_logs = json.loads(message).get("logs", False)
        except json.JSONDecodeError as e:
            self.LOGGER.warning("Socket JSON parsing error", exc_info=e)

    def on_keepalive(self):
        self.send_data({})

    def on_update_device(self, device):
        self.send_data({self.KEY_DEVICES: [device]})

    def on_update_position(self, position):
        self.send_data({self.KEY_POSITIONS: [position]})

    def on_update_event(self, event):
        self.send_data({self.KEY_EVENTS: [event]})

    def on_update_log(self, record):
        if self.include_logs:
            self.send_data({self.KEY_LOGS: [record]})

    def send_data(self, data):
        if self.is_connected():
            try:
                self.get_remote().send_string(self.object_mapper.dumps(data), None)
            except json.JSONDecodeError as e:
                self.LOGGER.warning("Socket JSON formatting error", exc_info=e)
