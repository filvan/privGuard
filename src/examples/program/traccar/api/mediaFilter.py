from src.examples.program.traccar.api.resource.sessionResource import SessionResource
from src.examples.program.traccar.api.security.permissionService import PermissionsService
from src.examples.program.traccar.database.statisticManager import StatisticsManager
from src.examples.program.traccar.helper.log import Log
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class MediaFilter():


    def __init__(self, storage, statisticsManager, permissionsServiceProvider):
        self._storage = None
        self._statisticsManager = None
        self._permissionsServiceProvider = None

        self._storage = storage
        self._statisticsManager = statisticsManager
        self._permissionsServiceProvider = permissionsServiceProvider

    def doFilter(self, request, response, chain):

        httpResponse = response
        try:
            session = (request).getSession(False)
            userId = None
            if session is not None:
                userId = int(session.getAttribute(SessionResource.USER_ID_KEY))
                if userId is not None:
                    self._statisticsManager.registerRequest(userId)
            if userId is None:
                httpResponse.sendError("HttpServletResponse.SC_UNAUTHORIZED")
                return

            path = (request).getPathInfo()
            parts = path.split("/") if path is not None else None
            if parts is not None and len(parts) >= 2:
                device = self._storage.getObject(Device.__class__, Request(Columns.All(), Condition.Equals("uniqueId", parts[1])))
                if device is not None:
                    self._permissionsServiceProvider.get().checkPermission(Device.__class__, userId, device.getId())
                    chain.doFilter(request, response)
                    return

            httpResponse.sendError("HttpServletResponse.SC_FORBIDDEN")
        except (Exception, StorageException) as e:
            httpResponse.setStatus("HttpServletResponse.SC_FORBIDDEN")
            httpResponse.getWriter().println(Log.exceptionStack(e))
