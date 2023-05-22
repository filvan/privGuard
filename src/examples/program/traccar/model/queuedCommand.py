from src.examples.program.traccar.storage.storageName import StorageName
from .baseCommand import BaseCommand

class QueuedCommand(BaseCommand):

    @staticmethod
    def fromCommand(command):
        queuedCommand = QueuedCommand()
        queuedCommand.setDeviceId(command.getDeviceId())
        queuedCommand.setType(command.getType())
        queuedCommand.setTextChannel(command.getTextChannel())
        queuedCommand.setAttributes(dict(command.getAttributes()))
        return queuedCommand

    def toCommand(self):
        command = self.Command()
        command.setDeviceId(self.getDeviceId())
        command.setType(self.getType())
        command.setDescription("")
        command.setTextChannel(self.getTextChannel())
        command.setAttributes(dict(self.getAttributes()))
        return command

