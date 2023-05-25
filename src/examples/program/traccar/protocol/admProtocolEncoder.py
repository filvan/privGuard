from src.examples.program.traccar.stringProtocolEncoder import StringProtocolEncoder
from src.examples.program.traccar.model.command import Command
from src.examples.program.traccar.protocol_file import Protocol

class AdmProtocolEncoder(StringProtocolEncoder):

    def __init__(self, protocol):
        super().__init__(protocol)

    def encodeCommand(self, command):

        if command.getType() == Command.TYPE_GET_DEVICE_STATUS:
            return self.formatCommand(command, "STATUS\r\n")

        elif command.getType() == Command.TYPE_CUSTOM:
            return self.formatCommand(command, "%s\r\n", Command.KEY_DATA)

        else:
            return None
