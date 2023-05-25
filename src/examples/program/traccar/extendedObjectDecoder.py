import collections

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.handler.ackowledgementHandler import AcknowledgementHandler
from src.examples.program.traccar.helper.dataConvereter import DataConverter
from src.examples.program.traccar.model.position import Position

class ExtendedObjectDecoder():

    def __init__(self):

        self._config = None



    def getConfig(self):
        return self._config

    def setConfig(self, config):
        self._config = config
        self.init()




    def init(self):
        pass

    def _saveOriginal(self, decodedMessage, originalMessage):
        if self.getConfig().getBoolean(Keys.DATABASE_SAVE_ORIGINAL) and isinstance(decodedMessage, Position):
            position = decodedMessage
            if isinstance(originalMessage, "ByteBuf"):
                buf = originalMessage
                position.set(Position.KEY_ORIGINAL, "ByteBufUtil.hexDump(buf, 0, buf.writerIndex())")
            elif isinstance(originalMessage, str):
                position.set(Position.KEY_ORIGINAL, DataConverter.printHex((str(originalMessage)).getBytes("us-ascii")))

    def channelRead(self, ctx, msg):
        networkMessage = msg
        originalMessage = networkMessage.getMessage()
        ctx.writeAndFlush(AcknowledgementHandler.EventReceived())
        try:
            decodedMessage = self.decode(ctx.channel(), networkMessage.getRemoteAddress(), originalMessage)
            self.onMessageEvent(ctx.channel(), networkMessage.getRemoteAddress(), originalMessage, decodedMessage)
            if decodedMessage is None:
                decodedMessage = self.handleEmptyMessage(ctx.channel(), networkMessage.getRemoteAddress(), originalMessage)
            if decodedMessage is not None:
                if isinstance(decodedMessage, collections):
                    collection = decodedMessage
                    ctx.writeAndFlush(AcknowledgementHandler.EventDecoded(collection))
                    for o in collection:
                        self._saveOriginal(o, originalMessage)
                        ctx.fireChannelRead(o)
                else:
                    ctx.writeAndFlush(AcknowledgementHandler.EventDecoded(list(decodedMessage)))
                    self._saveOriginal(decodedMessage, originalMessage)
                    ctx.fireChannelRead(decodedMessage)
            else:
                ctx.writeAndFlush(AcknowledgementHandler.EventDecoded(list()))
        finally:
            "ReferenceCountUtil.release(originalMessage)"

    def onMessageEvent(self, channel, remoteAddress, originalMessage, decodedMessage):
        pass

    def handleEmptyMessage(self, channel, remoteAddress, msg):
        return None

    def decode(self, channel, remoteAddress, msg):
        pass
