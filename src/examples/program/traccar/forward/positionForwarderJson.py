from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys

from .positionForwarder import PositionForwarder

class PositionForwarderJson(PositionForwarder):



    def __init__(self, config, client, objectMapper):
        self._url = None
        self._header = None
        self._client = None
        self._objectMapper = None

        self._client = client
        self._objectMapper = objectMapper
        self._url = config.getString(Keys.FORWARD_URL)
        self._header = config.getString(Keys.FORWARD_HEADER)

    def forward(self, positionData, resultHandler):
        requestBuilder = self._client.target(self._url).request()

        mediaType = "MediaType.APPLICATION_JSON_TYPE"
        if self._header is not None and self._header:
            for line in self._header.split("\\r?\\n"):
                values = line.split(":", 2)
                headerName = values[0].trim()
                headerValue = values[1].trim()
                if headerName == "HttpHeaders.CONTENT_TYPE":
                    mediaType = "MediaType.valueOf(headerValue)"
                else:
                    requestBuilder.header(headerName, headerValue)

        try:
            entity = "Entity.entity(self._objectMapper.writeValueAsString(positionData), mediaType)"
            requestBuilder.async_().post(entity, "InvocationCallbackAnonymousInnerClass(self, resultHandler)")
        except Exception as e:
            resultHandler.onResult(False, e)

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
