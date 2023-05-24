class UserSecurityContext():


    def __init__(self, principal):
        self._principal = None

        self._principal = principal

    def getUserPrincipal(self):
        return self._principal

    def isUserInRole(self, role):
        return True

    def isSecure(self):
        return False

    def getAuthenticationScheme(self):
        return BASIC_AUTH
