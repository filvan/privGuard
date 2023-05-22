from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys

from .eventForwarder import EventForwarder

class EventForwarderJson(EventForwarder):



    def __init__(self, config, client):
        self._url = None
        self._header = None
        self._client = None

        self._client = client
        self._url = config.getString(Keys.EVENT_FORWARD_URL)
        self._header = config.getString(Keys.EVENT_FORWARD_HEADERS)

    def forward(self, eventData, resultHandler):
        requestBuilder = self._client.target(self._url).request()

        if self._header is not None and self._header:
            for line in self._header.split("\\r?\\n"):
                values = line.split(":", 2)
                requestBuilder.header(values[0].trim(), values[1].trim())

        #requestBuilder.async_().post(Entity.json(eventData), InvocationCallbackAnonymousInnerClass(self, resultHandler))

    class InvocationCallbackAnonymousInnerClass():


        def __init__(self, outerInstance, resultHandler):
            self._outerInstance = outerInstance
            self._resultHandler = resultHandler

        def completed(self, response):
            if response.getStatusInfo().getFamily() == "Response.Status.Family.SUCCESSFUL":
                self._resultHandler.onResult(True, None)
            else:
                code = response.getStatusInfo().getStatusCode()
                self._resultHandler.onResult(False, Exception("HTTP code " + str(code)))

        def failed(self, throwable):
            self._resultHandler.onResult(False, throwable)
