from src.examples.program.traccar.api.security.serviceAccountUser import ServiceAccountUser
from src.examples.program.traccar.api.signature.tokenManager import TokenManager
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.database.ldapProvider import LdapProvider
from src.examples.program.traccar.helper.model.userUtil import UserUtil
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class LoginService:



    def __init__(self, config, storage, tokenManager, ldapProvider):

        self._config = None
        self._storage = None
        self._tokenManager = None
        self._ldapProvider = None
        self._serviceAccountToken = None
        self._forceLdap = False
        self._forceOpenId = False

        self._storage = storage
        self._config = config
        self._tokenManager = tokenManager
        self._ldapProvider = ldapProvider
        self._serviceAccountToken = config.getString(Keys.WEB_SERVICE_ACCOUNT_TOKEN)
        self._forceLdap = config.getBoolean(Keys.LDAP_FORCE)
        self._forceOpenId = config.getBoolean(Keys.OPENID_FORCE)

    def login(self, token):
        if self._serviceAccountToken is not None and self._serviceAccountToken == token:
            return ServiceAccountUser()
        userId = self._tokenManager.verifyToken(token)
        user = self._storage.getObject(User.__class__, Request(Columns.All(), Condition.Equals("id", userId)))
        if user is not None:
            self._checkUserEnabled(user)
        return user

    def login(self, email, password):
        if self._forceOpenId:
            return None

        email = email.trim()
        user = self._storage.getObject(User.__class__, Request(Columns.All(), Condition.Or(Condition.Equals("email", email), Condition.Equals("login", email))))
        if user is not None:
            if self._ldapProvider is not None and user.getLogin() is not None and self._ldapProvider.login(user.getLogin(), password) or (not self._forceLdap) and user.isPasswordValid(password):
                self._checkUserEnabled(user)
                return user
        else:
            if self._ldapProvider is not None and self._ldapProvider.login(email, password):
                user = self._ldapProvider.getUser(email)
                user.setId(self._storage.addObject(user, Request(Columns.Exclude("id"))))
                self._checkUserEnabled(user)
                return user
        return None

    def login(self, email, name, administrator):
        user = self._storage.getObject(User.__class__, Request(Columns.All(), Condition.Equals("email", email)))

        if user is not None:
            self._checkUserEnabled(user)
            return user
        else:
            user = User()
            UserUtil.setUserDefaults(user, self._config)
            user.setName(name)
            user.setEmail(email)
            user.setFixedEmail(True)
            user.setAdministrator(administrator)
            user.setId(self._storage.addObject(user, Request(Columns.Exclude("id"))))
            self._checkUserEnabled(user)
            return user

    def _checkUserEnabled(self, user):
        if user is None:
            raise Exception("Unknown account")
        user.checkDisabled()
