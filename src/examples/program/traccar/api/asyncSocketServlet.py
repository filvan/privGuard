from kafka.protocol.api import Response

from src.examples.program.traccar.api.resource.sessionResource import SessionResource
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.session.connectionManager import ConnectionManager
from src.examples.program.traccar.storage.storage import Storage


class AsyncSocketServlet():


    def __init__(self, config, objectMapper, connectionManager, storage):
        self._config = None
        self._objectMapper = None
        self._connectionManager = None
        self._storage = None

        self._config = config
        self._objectMapper = objectMapper
        self._connectionManager = connectionManager
        self._storage = storage

    def configure(self, factory):
        factory.setIdleTimeout(Duration.ofMillis(self._config.getLong(Keys.WEB_TIMEOUT)))
        #JAVA TO PYTHON CONVERTER TASK: Only expression lambdas are converted by Java to Python Converter:
        #        factory.setCreator((req, resp) ->
        #        {
        #            if (req.getSession() != null)
        #            {
        #                Long userId = (Long)((HttpSession) req.getSession()).getAttribute(SessionResource.USER_ID_KEY)
        #                if (userId != null)
        #                {
        #                    return new AsyncSocket(objectMapper, connectionManager, storage, userId)
        #                }
        #            }
        #            return null
        #        }
        #        )


