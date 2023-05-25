from numpy import array

from src.examples.program.traccar.helper.dataConvereter import DataConverter
from src.examples.program.traccar.model.command import Command
from src.examples.program.traccar.networkMessage import NetworkMessage
from src.examples.program.traccar.sms.smsManager import SmsManager
from src.examples.program.traccar.protocol_file import Protocol

class BaseProtocol(Protocol):




    @staticmethod
    def nameFromClass(clazz):
        className = clazz.getSimpleName()
        return className[0:len(className) - 8].toLowerCase()

    def __init__(self):

        self._name = None
        self._supportedDataCommands = array()
        self._supportedTextCommands = array()
        self._connectorList = []
        self._smsManager = None
        self._textCommandEncoder = None

        self._name = BaseProtocol.__class__.getName()

    def setSmsManager(self, smsManager):
        self._smsManager = smsManager

    def getName(self):
        return self._name

    def addServer(self, server):
        self._connectorList.append(server)

    def addClient(self, client):
        self._connectorList.append(client)

    def getConnectorList(self):
        return self._connectorList

    def setSupportedDataCommands(self, *commands):
        self._supportedDataCommands.addAll(array(commands))

    def setSupportedTextCommands(self, *commands):
        self._supportedTextCommands.addAll(array(commands))

    def getSupportedDataCommands(self):
        commands = array(self._supportedDataCommands)
        commands.add(Command.TYPE_CUSTOM)
        return commands

    def getSupportedTextCommands(self):
        commands = array(self._supportedTextCommands)
        commands.add(Command.TYPE_CUSTOM)
        return commands

    def sendDataCommand(self, channel, remoteAddress, command):
        if self._supportedDataCommands.contains(command.getType()):
            channel.writeAndFlush(NetworkMessage(command, remoteAddress))
        elif command.getType() is Command.TYPE_CUSTOM:
            data = command.getString(Command.KEY_DATA)
            if "BasePipelineFactory.getHandler(channel.pipeline(), StringEncoder.__class__)" is not None:
                channel.writeAndFlush(NetworkMessage(data, remoteAddress))
            else:
                buf =" Unpooled.wrappedBuffer(DataConverter.parseHex(data))"
                channel.writeAndFlush(NetworkMessage(buf, remoteAddress))
        else:
            raise Exception("Command " + command.getType() + " is not supported in protocol " + self.getName())

    def setTextCommandEncoder(self, textCommandEncoder):
        self._textCommandEncoder = textCommandEncoder

    def sendTextCommand(self, destAddress, command):
        if self._smsManager is not None:
            if command.getType() is Command.TYPE_CUSTOM:
                self._smsManager.sendMessage(destAddress, command.getString(Command.KEY_DATA), True)
            elif self._supportedTextCommands.contains(command.getType()) and self._textCommandEncoder is not None:
                encodedCommand = str(self._textCommandEncoder.encodeCommand(command))
                if encodedCommand is not None:
                    self._smsManager.sendMessage(destAddress, encodedCommand, True)
                else:
                    raise Exception("Failed to encode command")
            else:
                raise Exception("Command " + command.getType() + " is not supported in protocol " + self.getName())
        else:
            raise Exception("SMS is not enabled")
