from src.examples.program.traccar.api.security.permissionService import PermissionsService
from src.examples.program.traccar.api.security.userPrincipal import UserPrincipal
from src.examples.program.traccar.storage.storage import Storage


class BaseResource:

    def __init__(self):
        self.security_context = None
        self.storage = None
        self.permissions_service = None

    def get_user_id(self):
        principal = self.security_context.getUserPrincipal()
        if principal is not None:
            return principal.get_user_id()
        return 0
