from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys

class ConsoleServlet():

    _LOGGER = "LoggerFactory.getLogger(ConsoleServlet.__class__)"


    def __init__(self, config):
        self._config = None

        self._config = config

    def init(self):
        super().init()

        try:
            field = "WebServlet".__class__.getDeclaredField("server")
            field.setAccessible(True)
            server = field.get(self)

            connectionInfo = "ConnectionInfo(\"Traccar|\" + self._config.getString(Keys.DATABASE_DRIVER) + \"|\" + self._config.getString(Keys.DATABASE_URL) + \"|\" + self._config.getString(Keys.DATABASE_USER))"

            method = None

            method = self.org.h2.server.web.WebServer.__class__.getDeclaredMethod("updateSetting", "ConnectionInfo.__class__")
            method.setAccessible(True)
            method.invoke(server, connectionInfo)

            method = self.org.h2.server.web.WebServer.__class__.getDeclaredMethod("setAllowOthers", bool.__class__)
            method.setAccessible(True)
            method.invoke(server, True)

        except (BaseException, Exception) as e:
            ConsoleServlet._LOGGER.warn("Console reflection error", e)
