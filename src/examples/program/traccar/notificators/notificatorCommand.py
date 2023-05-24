from src.examples.program.traccar.database.commandsManager import CommandsManager
from src.examples.program.traccar.model.command import Command
from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.notification import Notification
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.notification.messageException import MessageException
from src.examples.program.traccar.notificators.notificator import Notificator
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class NotificatorCommand(Notificator):


    def __init__(self, storage, commandsManager):

        self._storage = None
        self._commandsManager = None

        self._storage = storage
        self._commandsManager = commandsManager

    def send(self, notification, user, event, position):

        if notification is None or notification.getCommandId() <= 0:
            raise MessageException("Saved command not provided")

        try:
            command = self._storage.getObject(Command.__class__, Request(Columns.All(), Condition.Equals("id", notification.getCommandId())))
            command.setDeviceId(event.getDeviceId())
            self._commandsManager.sendCommand(command)
        except Exception as e:
            raise MessageException(e)
