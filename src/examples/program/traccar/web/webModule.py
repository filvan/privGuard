from src.examples.program.traccar.api.asyncSocketServlet import AsyncSocketServlet
from src.examples.program.traccar.api.mediaFilter import MediaFilter
from src.examples.program.traccar.web.overrideFilter import OverrideFilter
from src.examples.program.traccar.web.throttlingFilter import ThrottlingFilter


class WebModule():

    def configureServlets(self):
        filter("/*").through(OverrideFilter.__class__)
        filter("/api/*").through(ThrottlingFilter.__class__)
        filter("/api/media/*").through(MediaFilter.__class__)
        self.serve("/api/socket").with_(AsyncSocketServlet.__class__)
