from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys


class ThrottlingFilter():

    def __init__(self):

        self._config = None



    def init(self, filterConfig):
        super().init(filterConfig)
        if self._config.hasKey(Keys.WEB_MAX_REQUESTS_PER_SECOND):
            self.setMaxRequestsPerSec(self._config.getInteger(Keys.WEB_MAX_REQUESTS_PER_SECOND))

    def extractUserId(self, request):
        session = (request).getSession(False)
        if session is not None:
            userId = session.getAttribute("userId")
            return str(userId) if userId is not None else None
        return None
