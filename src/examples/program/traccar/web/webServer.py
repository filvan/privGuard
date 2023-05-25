import enum
from msilib.schema import File
from xml.dom.pulldom import ErrorHandler

from src.examples.program.traccar.lifecycleObject import LifecycleObject
from src.examples.program.traccar.api.corsResponseFilter import CorsResponseFilter
from src.examples.program.traccar.api.dateParameterConverterProvider import DateParameterConverterProvider
from src.examples.program.traccar.api.resourceErrorHandler import ResourceErrorHandler
from src.examples.program.traccar.api.resource.serverResource import ServerResource
from src.examples.program.traccar.api.security.securityRequestFilter import SecurityRequestFilter
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.helper.objectMapperContextResolver import ObjectMapperContextResolver
from src.examples.program.traccar.model.server import Server


class WebServer(LifecycleObject):

    _LOGGER = "LoggerFactory.getLogger(WebServer.__class__)"


    def __init__(self, injector, config):

        self._injector = None
        self._config = None
        self._server = None

        self._injector = injector
        self._config = config
        address = config.getString(Keys.WEB_ADDRESS)
        port = config.getInteger(Keys.WEB_PORT)
        if address is None:
            self._server = Server(port)
        else:
            self._server = Server("InetSocketAddress(address, port)")

        servletHandler = "ServletContextHandler(ServletContextHandler.SESSIONS)"
        "JettyWebSocketServletContainerInitializer.configure(servletHandler, None)"
        servletHandler.addFilter("GuiceFilter".__class__, "/*", enum.allOf("DispatcherType.__class__"))

        self._initApi(servletHandler)
        self._initSessionConfig(servletHandler)

        if config.getBoolean(Keys.WEB_CONSOLE):
            servletHandler.addServlet("ServletHolder(ConsoleServlet(config))", "/console/*")

        self._initWebApp(servletHandler)

        servletHandler.setErrorHandler(self.ErrorHandlerAnonymousInnerClass(self))

        handlers = list()
        self._initClientProxy(handlers)
        handlers.addHandler(servletHandler)
        handlers.addHandler("GzipHandler()")
        self._server.setHandler(handlers)

        if config.hasKey(Keys.WEB_REQUEST_LOG_PATH):
            logWriter = "RequestLogWriter(config.getString(Keys.WEB_REQUEST_LOG_PATH))"
            logWriter.setAppend(True)
            logWriter.setRetainDays(config.getInteger(Keys.WEB_REQUEST_LOG_RETAIN_DAYS))
            requestLog = "CustomRequestLog(logWriter, CustomRequestLog.NCSA_FORMAT)"
            self._server.setRequestLog(requestLog)

    class ErrorHandlerAnonymousInnerClass(ErrorHandler):

        def __init__(self, outerInstance):
            self._outerInstance = outerInstance

        def handleErrorPage(self, request, writer, code, message):
            writer.write("<!DOCTYPE><html><head><title>Error</title></head><html><body>" + str(code) + " - " + "HttpStatus.getMessage(code)" + "</body></html>")

    def _initClientProxy(self, handlers):
        port = self._config.getInteger(Keys.PROTOCOL_PORT.withPrefix("osmand"))
        if port != 0:
            servletHandler = self.ServletContextHandlerAnonymousInnerClass(self)
            servletHolder =" ServletHolder(AsyncProxyServlet.Transparent.__class__)"
            servletHolder.setInitParameter("proxyTo", "http://localhost:" + str(port))
            servletHandler.addServlet(servletHolder, "/")
            handlers.addHandler(servletHandler)

    class ServletContextHandlerAnonymousInnerClass():

        def __init__(self, outerInstance):
            self._outerInstance = outerInstance

        def doScope(self, target, baseRequest, request, response):
            if target == "/" and request.getMethod() is "HttpMethod.POST.asString()":
                super().doScope(target, baseRequest, request, response)

    def _initWebApp(self, servletHandler):
        servletHolder = "ServletHolder(ModernDefaultServlet(self._config))"
        servletHolder.setInitParameter("resourceBase", (File(self._config.getString(Keys.WEB_PATH))).getAbsolutePath())
        servletHolder.setInitParameter("dirAllowed", "false")
        if self._config.getBoolean(Keys.WEB_DEBUG):
            servletHandler.setWelcomeFiles(["debug.html", "index.html"])
        else:
            cache = self._config.getString(Keys.WEB_CACHE_CONTROL)
            if cache is not None and cache:
                servletHolder.setInitParameter("cacheControl", cache)
            servletHandler.setWelcomeFiles(["release.html", "index.html"])
        servletHandler.addServlet(servletHolder, "/*")

    def _initApi(self, servletHandler):
        mediaPath = self._config.getString(Keys.MEDIA_PATH)
        if mediaPath is not None:
            servletHolder = "ServletHolder(DefaultServlet.__class__)"
            servletHolder.setInitParameter("resourceBase", (File(mediaPath)).getAbsolutePath())
            servletHolder.setInitParameter("dirAllowed", "false")
            servletHolder.setInitParameter("pathInfoOnly", "true")
            servletHandler.addServlet(servletHolder, "/api/media/*")

        resourceConfig = "ResourceConfig()"
        resourceConfig.registerClasses("JacksonFeature.__class__, ObjectMapperContextResolver.__class__, DateParameterConverterProvider.__class__, SecurityRequestFilter.__class__, CorsResponseFilter.__class__, ResourceErrorHandler.__class__")
        resourceConfig.packages(ServerResource.__class__.getPackage().getName())
        if resourceConfig.getClasses().stream().filter(ServerResource.__class__.equals()).findAny().isEmpty():
            WebServer._LOGGER.warn("Failed to load API resources")
        servletHandler.addServlet("ServletHolder(ServletContainer(resourceConfig))", "/api/*")

    def _initSessionConfig(self, servletHandler):
        if self._config.getBoolean(Keys.WEB_PERSIST_SESSION):
            databaseAdaptor = "DatabaseAdaptor()"
            databaseAdaptor.setDatasource(self._injector.getInstance("DataSource.__class__"))
            jdbcSessionDataStoreFactory = "JDBCSessionDataStoreFactory()"
            jdbcSessionDataStoreFactory.setDatabaseAdaptor(databaseAdaptor)
            sessionHandler = servletHandler.getSessionHandler()
            sessionCache = "DefaultSessionCache(sessionHandler)"
            sessionCache.setSessionDataStore(jdbcSessionDataStoreFactory.getSessionDataStore(sessionHandler))
            sessionHandler.setSessionCache(sessionCache)

        sessionTimeout = self._config.getInteger(Keys.WEB_SESSION_TIMEOUT)
        if sessionTimeout > 0:
            servletHandler.getSessionHandler().setMaxInactiveInterval(sessionTimeout)

        sameSiteCookie = self._config.getString(Keys.WEB_SAME_SITE_COOKIE)
        if sameSiteCookie is not None:
            sessionCookieConfig = servletHandler.getServletContext().getSessionCookieConfig()
            if sameSiteCookie.casefold() == "lax":
                sessionCookieConfig.setComment("HttpCookie".SAME_SITE_LAX_COMMENT)
            elif sameSiteCookie.casefold() == "strict":
                sessionCookieConfig.setComment("HttpCookie".SAME_SITE_STRICT_COMMENT)
            elif sameSiteCookie.casefold() == "none":
                sessionCookieConfig.setSecure(True)
                sessionCookieConfig.setComment("HttpCookie".SAME_SITE_NONE_COMMENT)



    def start(self):
        self._server.start()



    def stop(self):
        self._server.stop()


