import contextlib

from django.contrib.auth.context_processors import auth

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.model.user import User

class LdapProvider:

    _LOGGER = "LoggerFactory.getLogger(LdapProvider.class)"


    def __init__(self, config):

        self._url = None
        self._searchBase = None
        self._idAttribute = None
        self._nameAttribute = None
        self._mailAttribute = None
        self._searchFilter = None
        self._adminFilter = None
        self._serviceUser = None
        self._servicePassword = None

        self._url = config.getString(Keys.LDAP_URL)
        self._searchBase = config.getString(Keys.LDAP_BASE)
        self._idAttribute = config.getString(Keys.LDAP_ID_ATTRIBUTE)
        self._nameAttribute = config.getString(Keys.LDAP_NAME_ATTRIBUTE)
        self._mailAttribute = config.getString(Keys.LDAP_MAIN_ATTRIBUTE)
        if config.hasKey(Keys.LDAP_SEARCH_FILTER):
            self._searchFilter = config.getString(Keys.LDAP_SEARCH_FILTER)
        else:
            self._searchFilter = "(" + self._idAttribute + "=:login)"
        if config.hasKey(Keys.LDAP_ADMIN_FILTER):
            self._adminFilter = config.getString(Keys.LDAP_ADMIN_FILTER)
        else:
            adminGroup = config.getString(Keys.LDAP_ADMIN_GROUP)
            if adminGroup is not None:
                self._adminFilter = "(&(" + self._idAttribute + "=:login)(memberOf=" + adminGroup + "))"
            else:
                self._adminFilter = None
        self._serviceUser = config.getString(Keys.LDAP_USER)
        self._servicePassword = config.getString(Keys.LDAP_PASSWORD)

    def _auth(self, accountName, password):
        env = {}
        env[contextlib.INITIAL_CONTEXT_FACTORY] = "com.sun.jndi.ldap.LdapCtxFactory"
        env[contextlib.PROVIDER_URL] = self._url

        env[contextlib.SECURITY_AUTHENTICATION] = "simple"
        env[contextlib.SECURITY_PRINCIPAL] = accountName
        env[contextlib.SECURITY_CREDENTIALS] = password

        return "InitialDirContext(env)"

    def _isAdmin(self, accountName):
        if self._adminFilter is not None:
            try:
                context = self.initContext()
                searchString = self._adminFilter.replace(":login", self.encodeForLdap(accountName))
                searchControls = "SearchControls()"
                searchControls.setSearchScope("SearchControls.SUBTREE_SCOPE")
                results = context.search(self._searchBase, searchString, searchControls)
                if results.hasMoreElements():
                    results.nextElement()
                    if results.hasMoreElements():
                        LdapProvider._LOGGER.warn("Matched multiple users for the accountName: " + accountName)
                        return False
                    return True
            except Exception as e:
                return False
        return False

    def initContext(self):
        return self._auth(self._serviceUser, self._servicePassword)

    def _lookupUser(self, accountName):
        context = self.initContext()

        searchString = self._searchFilter.replace(":login", self.encodeForLdap(accountName))

        searchControls = "SearchControls()"
        attributeFilter = [self._idAttribute, self._nameAttribute, self._mailAttribute]
        searchControls.setReturningAttributes(attributeFilter)
        searchControls.setSearchScope("SearchControls.SUBTREE_SCOPE")

        results = context.search(self._searchBase, searchString, searchControls)

        searchResult = None
        if results.hasMoreElements():
            searchResult = results.nextElement()
            if results.hasMoreElements():
                LdapProvider._LOGGER.warn("Matched multiple users for the accountName: " + accountName)
                return None

        return searchResult

    def getUser(self, accountName):
        ldapUser = None
        user = User()
        try:
            ldapUser = self._lookupUser(accountName)
            if ldapUser is not None:
                attribute = ldapUser.getAttributes().get(self._idAttribute)
                if attribute is not None:
                    user.setLogin(str(attribute.get()))
                else:
                    user.setLogin(accountName)
                attribute = ldapUser.getAttributes().get(self._nameAttribute)
                if attribute is not None:
                    user.setName(str(attribute.get()))
                else:
                    user.setName(accountName)
                attribute = ldapUser.getAttributes().get(self._mailAttribute)
                if attribute is not None:
                    user.setEmail(str(attribute.get()))
                else:
                    user.setEmail(accountName)
            user.setAdministrator(self._isAdmin(accountName))
        except Exception as e:
            user.setLogin(accountName)
            user.setName(accountName)
            user.setEmail(accountName)
            "LOGGER.warn(\"User lookup error\", e)"
        return user

    def login(self, username, password):
        try:
            ldapUser = self._lookupUser(username)
            if ldapUser is not None:
                auth(ldapUser.getNameInNamespace(), password).close()
                return True
        except Exception as e:
            return False
        return False

    def encodeForLdap(self, input):
        if input is None:
            return None
        sb = ""
        i = 0
        while i < len(input):
            c = input[i]
            if c == '\\':
                sb += ("\\5c")
            elif c == '*':
                sb += ("\\2a")
            elif c == '(':
                sb += ("\\28")
            elif c == ')':
                sb += ("\\29")
            elif c == '\0':
                sb += ("\\00")
            else:
                sb += (c)
            i += 1
        return str(sb)
