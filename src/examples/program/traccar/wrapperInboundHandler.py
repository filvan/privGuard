from src.examples.program.traccar.networkMessage import NetworkMessage
from src.examples.program.traccar.wrapperContext import WrapperContext


class WrapperInboundHandler():


    def getWrappedHandler(self):
        return self._handler

    def __init__(self, handler):

        self._handler = None

        self._handler = handler

    def channelRegistered(self, ctx):
        self._handler.channelRegistered(ctx)

    def channelUnregistered(self, ctx):
        self._handler.channelUnregistered(ctx)

    def channelActive(self, ctx):
        self._handler.channelActive(ctx)

    def channelInactive(self, ctx):
        self._handler.channelInactive(ctx)

    def channelRead(self, ctx, msg):
        if isinstance(msg, NetworkMessage):
            nm = msg
            self._handler.channelRead(WrapperContext(ctx, nm.getRemoteAddress()), nm.getMessage())
        else:
            self._handler.channelRead(ctx, msg)

    def channelReadComplete(self, ctx):
        self._handler.channelReadComplete(ctx)

    def userEventTriggered(self, ctx, evt):
        self._handler.userEventTriggered(ctx, evt)

    def channelWritabilityChanged(self, ctx):
        self._handler.channelWritabilityChanged(ctx)

    def handlerAdded(self, ctx):
        self._handler.handlerAdded(ctx)

    def handlerRemoved(self, ctx):
        self._handler.handlerRemoved(ctx)

    def exceptionCaught(self, ctx, cause):
        self._handler.exceptionCaught(ctx, cause)
