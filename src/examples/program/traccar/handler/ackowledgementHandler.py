from multiprocessing.sharedctypes import synchronized

from numpy import array


class AcknowledgementHandler():

    def __init__(self):

        self._queue = None
        self._waiting = array()


    _LOGGER = "LoggerFactory.getLogger(AcknowledgementHandler.class)"

    class Event:
        pass

    class EventReceived(Event):
        pass

    class EventDecoded(Event):

        def __init__(self, objects):

            self._objects = None

            self._objects = objects

        def getObjects(self):
            return self._objects

    class EventHandled(Event):

        def __init__(self, object):

            self._object = None

            self._object = object

        def getObject(self):
            return self._object

    class Entry:

        def __init__(self, message, promise):

            self._message = None
            self._promise = None

            self._message = message
            self._promise = promise

        def getMessage(self):
            return self._message

        def getPromise(self):
            return self._promise


    def write(self, ctx, msg, promise):
        output = []
        synchronized(self)
        if isinstance(msg, self.Event):
            if isinstance(msg, self.EventReceived):
                AcknowledgementHandler._LOGGER.debug("Event received")
                if self._queue is None:
                    self._queue = []
            elif isinstance(msg, self.EventDecoded):
                event = msg
                AcknowledgementHandler._LOGGER.debug("Event decoded {}", len(event.getObjects()))
                self._waiting.addAll(event.getObjects())
            elif isinstance(msg, self.EventHandled):
                event = msg
                AcknowledgementHandler._LOGGER.debug("Event handled")
                self._waiting.remove(event.getObject())
            if not(isinstance(msg, self.EventReceived)) and self._waiting.isEmpty():
                output.extend(self._queue)
                self._queue = None
        elif self._queue is not None:
            AcknowledgementHandler._LOGGER.debug("Message queued")
            self._queue.append(self.Entry(msg, promise))
        else:
            AcknowledgementHandler._LOGGER.debug("Message sent")
            output.append(self.Entry(msg, promise))
        for entry in output:
            ctx.write(entry.getMessage(), entry.getPromise())
