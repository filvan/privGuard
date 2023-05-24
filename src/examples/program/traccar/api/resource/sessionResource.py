import urllib

from kafka.protocol.api import Response
from oauthlib.uri_validate import URI

from src.examples.program.traccar.api.baseResource import BaseResource
from src.examples.program.traccar.api.security.loginService import LoginService
from src.examples.program.traccar.api.signature.tokenManager import TokenManager
from src.examples.program.traccar.database.openIdProvider import OpenIdProvider
from src.examples.program.traccar.helper.dataConvereter import DataConverter
from src.examples.program.traccar.helper.logAction import LogAction
from src.examples.program.traccar.helper.webHelper import WebHelper
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class SessionResource(BaseResource):

    def __init__(self):

        self._loginService = None
        self._openIdProvider = None
        self._tokenManager = None
        self._request = None


    USER_ID_KEY = "userId"
    USER_COOKIE_KEY = "user"
    PASS_COOKIE_KEY = "password"

    def get(self, token):

        if token is not None:
            user = self._loginService.login(token)
            if user is not None:
                self._request.getSession().setAttribute(SessionResource.USER_ID_KEY, user.getId())
                LogAction.login(user.getId(), WebHelper.retrieveRemoteAddress(self._request))
                return user

        userId = int(self._request.getSession().getAttribute(SessionResource.USER_ID_KEY))
        if userId is None:

            cookies = self._request.getCookies()
            email = None
            password = None
            if cookies is not None:
                for cookie in cookies:
                    if cookie.getName() is SessionResource.USER_COOKIE_KEY:
                        emailBytes = DataConverter.parseBase64(urllib.decode(cookie.getValue(), "us-ascii"))
                        email = str(emailBytes, "utf-8")
                    elif cookie.getName() is SessionResource.PASS_COOKIE_KEY:
                        passwordBytes = DataConverter.parseBase64(urllib.decode(cookie.getValue(), "us-ascii"))
                        password = str(passwordBytes, "utf-8")
            if email is not None and password is not None:
                user = self._loginService.login(email, password)
                if user is not None:
                    self._request.getSession().setAttribute(SessionResource.USER_ID_KEY, user.getId())
                    LogAction.login(user.getId(), WebHelper.retrieveRemoteAddress(self._request))
                    return user

        else:

            user = BaseResource.permissionsService.getUser(userId)
            if user is not None:
                return user


        raise Exception(Response.status(Response.Status.NOT_FOUND).build())

    def get(self, userId):
        BaseResource.permissionsService.checkUser(BaseResource.getUserId(), userId)
        user = BaseResource.storage.getObject(User.__class__, Request(Columns.All(), Condition.Equals("id", userId)))
        self._request.getSession().setAttribute(SessionResource.USER_ID_KEY, user.getId())
        LogAction.login(user.getId(), WebHelper.retrieveRemoteAddress(self._request))
        return user

    def add(self, email, password):
        user = self._loginService.login(email, password)
        if user is not None:
            self._request.getSession().setAttribute(SessionResource.USER_ID_KEY, user.getId())
            LogAction.login(user.getId(), WebHelper.retrieveRemoteAddress(self._request))
            return user
        else:
            LogAction.failedLogin(WebHelper.retrieveRemoteAddress(self._request))
            raise Exception(Response.status(Response.Status.UNAUTHORIZED).build())

    def remove(self):
        LogAction.logout(BaseResource.getUserId(), WebHelper.retrieveRemoteAddress(self._request))
        self._request.getSession().removeAttribute(SessionResource.USER_ID_KEY)
        return Response.noContent().build()

    def requestToken(self, expiration):
        return self._tokenManager.generateToken(BaseResource.getUserId(), expiration)

    def openIdAuth(self):
        return Response.seeOther(self._openIdProvider.createAuthUri()).build()

    def requestToken(self):
        requestUrl = str(self._request.getRequestURL())
        queryString = self._request.getQueryString()
        requestUri = str(requestUrl+ '?' +queryString)

        return Response.seeOther(self._openIdProvider.handleCallback(URI.create(requestUri), self._request)).build()
