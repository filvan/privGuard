from src.examples.program.traccar.networkMessage import NetworkMessage
from src.examples.program.traccar.wrapperContext import WrapperContext


class WrapperOutboundHandler():


    def getWrappedHandler(self):
        return self._handler

    def __init__(self, handler):

        self._handler = None

        self._handler = handler

    def bind(self, ctx, localAddress, promise):
        self._handler.bind(ctx, localAddress, promise)

    def connect(self, ctx, remoteAddress, localAddress, promise):
        self._handler.connect(ctx, remoteAddress, localAddress, promise)

    def disconnect(self, ctx, promise):
        self._handler.disconnect(ctx, promise)

    def close(self, ctx, promise):
        self._handler.close(ctx, promise)

    def deregister(self, ctx, promise):
        self._handler.deregister(ctx, promise)

    def read(self, ctx):
        self._handler.read(ctx)

    def write(self, ctx, msg, promise):
        if isinstance(msg, NetworkMessage):
            nm = msg
            self._handler.write(WrapperContext(ctx, nm.getRemoteAddress()), nm.getMessage(), promise)
        else:
            self._handler.write(ctx, msg, promise)

    def flush(self, ctx):
        self._handler.flush(ctx)

    def handlerAdded(self, ctx):
        self._handler.handlerAdded(ctx)

    def handlerRemoved(self, ctx):
        self._handler.handlerRemoved(ctx)

    def exceptionCaught(self, ctx, cause):
        self._handler.exceptionCaught(ctx, cause)
