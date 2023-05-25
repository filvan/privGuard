from src.examples.program.traccar.networkMessage import NetworkMessage


class WrapperContext():


    def __init__(self, context, remoteAddress):

        self._context = None
        self._remoteAddress = None

        self._context = context
        self._remoteAddress = remoteAddress

    def channel(self):
        return self._context.channel()

    def executor(self):
        return self._context.executor()

    def name(self):
        return self._context.name()

    def handler(self):
        return self._context.handler()

    def isRemoved(self):
        return self._context.isRemoved()

    def fireChannelRegistered(self):
        return self._context.fireChannelRegistered()

    def fireChannelUnregistered(self):
        return self._context.fireChannelUnregistered()

    def fireChannelActive(self):
        return self._context.fireChannelActive()

    def fireChannelInactive(self):
        return self._context.fireChannelInactive()

    def fireExceptionCaught(self, cause):
        return self._context.fireExceptionCaught(cause)

    def fireUserEventTriggered(self, evt):
        return self._context.fireUserEventTriggered(evt)

    def fireChannelRead(self, msg):
        if not(isinstance(msg, NetworkMessage)):
            msg = NetworkMessage(msg, self._remoteAddress)
        return self._context.fireChannelRead(msg)

    def fireChannelReadComplete(self):
        return self._context.fireChannelReadComplete()

    def fireChannelWritabilityChanged(self):
        return self._context.fireChannelWritabilityChanged()

    def bind(self, localAddress):
        return self._context.bind(localAddress)

    def connect(self, remoteAddress):
        return self._context.connect(remoteAddress)

    def connect(self, remoteAddress, localAddress):
        return self._context.connect(remoteAddress, localAddress)

    def disconnect(self):
        return self._context.disconnect()

    def close(self):
        return self._context.close()

    def deregister(self):
        return self._context.deregister()

    def bind(self, localAddress, promise):
        return self._context.bind(localAddress, promise)

    def connect(self, remoteAddress, promise):
        return self._context.connect(remoteAddress, promise)

    def connect(self, remoteAddress, localAddress, promise):
        return self._context.connect(remoteAddress, localAddress, promise)

    def disconnect(self, promise):
        return self._context.disconnect(promise)

    def close(self, promise):
        return self._context.close(promise)

    def deregister(self, promise):
        return self._context.deregister(promise)

    def read(self):
        return self._context.read()

    def write(self, msg):
        return self._context.write(msg)

    def write(self, msg, promise):
        if not(isinstance(msg, NetworkMessage)):
            msg = NetworkMessage(msg, self._remoteAddress)
        return self._context.write(msg, promise)

    def flush(self):
        return self._context.flush()

    def writeAndFlush(self, msg, promise):
        return self._context.writeAndFlush(msg, promise)

    def writeAndFlush(self, msg):
        return self._context.writeAndFlush(msg)

    def newPromise(self):
        return self._context.newPromise()

    def newProgressivePromise(self):
        return self._context.newProgressivePromise()

    def newSucceededFuture(self):
        return self._context.newSucceededFuture()

    def newFailedFuture(self, cause):
        return self._context.newFailedFuture(cause)

    def voidPromise(self):
        return self._context.voidPromise()

    def pipeline(self):
        return self._context.pipeline()

    def alloc(self):
        return self._context.alloc()

    def attr(self, key):
        return self._context.attr(key)

    def hasAttr(self, key):
        return self._context.hasAttr(key)
