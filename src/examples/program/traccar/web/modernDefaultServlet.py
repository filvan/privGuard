from importlib.resources import Resource
from msilib.schema import File

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys

class ModernDefaultServlet():


    def __init__(self, config):

        self._overrideResource = None

        override = config.getString(Keys.WEB_OVERRIDE)
        if override is not None:
            self._overrideResource = Resource.newResource(File(override))

    def getResource(self, pathInContext):
        if self._overrideResource is not None:
            try:
                override = self._overrideResource.addPath(pathInContext)
                if override.exists():
                    return override
            except FileExistsError as e:
                raise Exception(e)
        return super().getResource("/" if pathInContext.find('.') < 0 else pathInContext)

    def getWelcomeFile(self, pathInContext):
        return super().getWelcomeFile("/")
