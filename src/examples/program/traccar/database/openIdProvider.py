from sre_parse import State

from django.http import HttpRequest
from jinja2.nodes import Scope
from oauthlib.openid.connect.core.grant_types import AuthorizationCodeGrant
from oauthlib.uri_validate import URI

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.api.resource.sessionResource import SessionResource
from src.examples.program.traccar.api.security.loginService import LoginService
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.helper.logAction import LogAction
from src.examples.program.traccar.helper.webHelper import WebHelper


class OpenIdProvider:


    def __init__(self, config, loginService, httpClient, objectMapper):

        self._force = False
        self._clientId = None
        self._clientAuth = None
        self._callbackUrl = None
        self._authUrl = None
        self._tokenUrl = None
        self._userInfoUrl = None
        self._baseUrl = None
        self._adminGroup = None
        self._allowGroup = None
        self._loginService = None

        self._loginService = loginService

        self._force = config.getBoolean(Keys.OPENID_FORCE)
        self._clientId = "ClientID(config.getString(Keys.OPENID_CLIENT_ID))"
        self._clientAuth = "ClientSecretBasic(self._clientId, Secret(config.getString(Keys.OPENID_CLIENT_SECRET)))"

        self._baseUrl = URI(WebHelper.retrieveWebUrl(config))
        self._callbackUrl = URI(WebHelper.retrieveWebUrl(config) + "/api/session/openid/callback")

        if config.hasKey(Keys.OPENID_ISSUER_URL):
            httpRequest = HttpRequest.newBuilder(URI.create(config.getString(Keys.OPENID_ISSUER_URL) + "/.well-known/openid-configuration")).header("Accept", "application/json").build()

            httpResponse = httpClient.send(httpRequest," BodyHandlers.ofString()").body()

            discoveryMap = objectMapper.readValue(httpResponse," TypeReferenceAnonymousInnerClass(self)")

            self._authUrl = URI(str(discoveryMap["authorization_endpoint"]))
            self._tokenUrl = URI(str(discoveryMap["token_endpoint"]))
            self._userInfoUrl = URI(str(discoveryMap["userinfo_endpoint"]))
        else:
            self._authUrl = URI(config.getString(Keys.OPENID_AUTH_URL))
            self._tokenUrl = URI(config.getString(Keys.OPENID_TOKEN_URL))
            self._userInfoUrl = URI(config.getString(Keys.OPENID_USERINFO_URL))

        self._adminGroup = config.getString(Keys.OPENID_ADMIN_GROUP)
        self._allowGroup = config.getString(Keys.OPENID_ALLOW_GROUP)

    class TypeReferenceAnonymousInnerClass("TypeReference"):

        def __init__(self, outerInstance):
            self._outerInstance = outerInstance


    def createAuthUri(self):
        scope = Scope("openid", "profile", "email")

        if self._adminGroup is not None:
            scope.add("groups")

        request = "AuthenticationRequest.Builder(ResponseType(\"code\"), scope, self._clientId, self._callbackUrl)"

        return request.endpointURI(self._authUrl).state(State()).build().toURI()

    def _getToken(self, code):
        codeGrant = AuthorizationCodeGrant(code, self._callbackUrl)
        tokenRequest = "TokenRequest(self._tokenUrl, self._clientAuth, codeGrant)"

        tokenResponse = tokenRequest.toHTTPRequest().send()
        token = "OIDCTokenResponseParser.parse(tokenResponse)"
        if not token.indicatesSuccess():
            raise Exception("Unable to authenticate with the OpenID Connect provider.")

        return token.toSuccessResponse()

    def _getUserInfo(self, token):
        httpResponse = "(UserInfoRequest(self._userInfoUrl, token)).toHTTPRequest().send()"

        userInfoResponse = "UserInfoResponse.parse(httpResponse)"

        if not userInfoResponse.indicatesSuccess():
            raise Exception("Failed to access OpenID Connect user info endpoint. Please contact your administrator.")

        return userInfoResponse.toSuccessResponse().getUserInfo()

    def handleCallback(self, requestUri, request):
        response = "AuthorizationResponse.parse(requestUri)"

        if not response.indicatesSuccess():
            raise Exception(response.toErrorResponse().getErrorObject().getDescription())

        authCode = response.toSuccessResponse().getAuthorizationCode()

        if authCode is None:
            raise Exception("Malformed OpenID callback.")

        tokens = self._getToken(authCode)

        bearerToken = tokens.getOIDCTokens().getBearerAccessToken()

        userInfo = self._getUserInfo(bearerToken)

        userGroups = userInfo.getStringListClaim("groups")
        administrator = self._adminGroup is not None and self._adminGroup in userGroups

        if not(administrator or self._allowGroup is None or self._allowGroup in userGroups):
            raise Exception("Your OpenID Groups do not permit access to Traccar.")

        user = self._loginService.login(userInfo.getEmailAddress(), userInfo.getName(), administrator)

        request.getSession().setAttribute(SessionResource.USER_ID_KEY, user.getId())
        LogAction.login(user.getId(), WebHelper.retrieveRemoteAddress(request))

        return self._baseUrl

    def getForce(self):
        return self._force
