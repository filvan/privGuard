from src.examples.program.traccar.api.security.permissionService import PermissionsService
from src.examples.program.traccar.api.security.userPrincipal import UserPrincipal
from src.examples.program.traccar.storage.storage import Storage

class BaseResource:

    def __init__(self):
        self._securityContext = None
        self.storage = None
        self.permissionsService = None





    def getUserId(self):
        principal = self._securityContext.getUserPrincipal()
        if principal is not None:
            return principal.getUserId()
        return 0
