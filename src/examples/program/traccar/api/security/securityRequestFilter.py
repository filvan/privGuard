from kafka.protocol.api import Response

from src.examples.program.traccar.api.resource.sessionResource import SessionResource
from src.examples.program.traccar.api.security.permissionService import PermissionsService
from src.examples.program.traccar.api.security.userPrincipal import UserPrincipal
from src.examples.program.traccar.api.security.userSecurityContext import UserSecurityContext
from src.examples.program.traccar.database.statisticManager import StatisticsManager
from src.examples.program.traccar.helper.dataConvereter import DataConverter
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.storage.storageException import StorageException


class SecurityRequestFilter():

    def __init__(self):

        self._request = None
        self._resourceInfo = None
        self._loginService = None
        self._statisticsManager = None
        self._injector = None


    _LOGGER = "LoggerFactory.getLogger(SecurityRequestFilter.class)"

    @staticmethod
    def decodeBasicAuth(auth):
        auth = auth.replaceFirst("[B|b]asic ", "")
        decodedBytes = DataConverter.parseBase64(auth)
        if decodedBytes is not None and len(decodedBytes) > 0:
            return (str(decodedBytes, "us-acii")).split(":", 2)
        return None






    def filter(self, requestContext):

        if requestContext.getMethod() is "OPTIONS":
            return

        securityContext = None

        try:

            authHeader = requestContext.getHeaderString("Authorization")
            if authHeader is not None:

                try:
                    user = None
                    if authHeader.startswith("Bearer "):
                        user = self._loginService.login(authHeader[7:])
                    else:
                        auth = SecurityRequestFilter.decodeBasicAuth(authHeader)
                        user = self._loginService.login(auth[0], auth[1])
                    if user is not None:
                        self._statisticsManager.registerRequest(user.getId())
                        securityContext = UserSecurityContext(UserPrincipal(user.getId()))
                except (StorageException, Exception) as e:
                    raise Exception(e)

            elif self._request.getSession() is not None:

                userId = int(self._request.getSession().getAttribute(SessionResource.USER_ID_KEY))
                if userId is not None:
                    self._injector.getInstance(PermissionsService.__class__).getUser(userId).checkDisabled()
                    self._statisticsManager.registerRequest(userId)
                    securityContext = UserSecurityContext(UserPrincipal(userId))


        except (Exception, StorageException) as e:
            SecurityRequestFilter._LOGGER.warn("Authentication error", e)

        if securityContext is not None:
            requestContext.setSecurityContext(securityContext)
        else:
            method = self._resourceInfo.getResourceMethod()
            if not method.isAnnotationPresent("PermitAll".__class__):
                responseBuilder = Response.status(Response.Status.UNAUTHORIZED)
                accept = self._request.getHeader("Accept")
                if accept is not None and "text/html" in accept:
                    responseBuilder.header("WWW-Authenticate", "Basic realm=\"api\"")
                raise Exception(responseBuilder.build())
