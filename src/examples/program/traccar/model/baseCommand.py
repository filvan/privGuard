from .message import Message

class BaseCommand(Message):

    def __init__(self):
        self._textChannel = False

    def getTextChannel(self):
        return self._textChannel

    def setTextChannel(self, textChannel):
        self._textChannel = textChannel
