from src.examples.program.traccar.baseProtocolEncoder import BaseProtocolEncoder
from src.examples.program.traccar.model.command import Command

class StringProtocolEncoder(BaseProtocolEncoder):

    def __init__(self, protocol):
        super().__init__(protocol)

    class ValueFormatter:
        def formatValue(self, key, value):
            pass

    def formatCommand(self, command, format, valueFormatter, *keys):

        values = [None for _ in range(len(keys))]
        i = 0
        while i < len(keys):
            value = None
            if keys[i] == Command.KEY_UNIQUE_ID:
                value = self.getUniqueId(command.getDeviceId())
            else:
                object = command.getAttributes().get(keys[i])
                if valueFormatter is not None:
                    value = valueFormatter.formatValue(keys[i], object)
                if value is None and object is not None:
                    value = str(object)
                if value is None:
                    value = ""
            values[i] = value
            i += 1

        return str.format(format, values)

    def formatCommand(self, command, format, *keys):
        return self.formatCommand(command, format, None, keys)
