import json
from src.examples.program.traccar.api.asyncSocket import AsyncSocket
from src.examples.program.traccar.api.resource.sessionResource import SessionResource
from src.examples.program.traccar.api.security import loginService
from src.examples.program.traccar.config import config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.session import connectionManager
from src.examples.program.traccar.storage import storage, storageException


class AsyncSocketServlet:

    def __init__(self, config, object_mapper, connection_manager, storage, login_service):
        self.config = config
        self.object_mapper = object_mapper
        self.connection_manager = connection_manager
        self.storage = storage
        self.login_service = login_service

    def configure(self):
        self.set_idle_timeout(self.config.get_long(Keys.WEB_TIMEOUT))
        self.set_creator(self.create_socket)

    def create_socket(self, req, resp):
        user_id = None
        tokens = req.get('token', [])
        if tokens:
            token = tokens[0]
            try:
                user_id = self.login_service.login(token).get_user().get_id()
            except (storageException, IOError) as e:
                raise RuntimeError(e)
        elif req.get('session') is not None:
            user_id = req.get('session').get(SessionResource.USER_ID_KEY)
        if user_id is not None:
            return AsyncSocket(self.object_mapper, self.connection_manager, self.storage, user_id)
        return None
