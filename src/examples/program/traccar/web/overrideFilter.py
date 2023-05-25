from logging import Filter

from src.examples.program.traccar.api.security.permissionService import PermissionsService
from src.examples.program.traccar.model.server import Server
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.web.responseWrapper import ResponseWrapper


class OverrideFilter(Filter):


    def __init__(self, permissionsServiceProvider):

        self._permissionsServiceProvider = None

        self._permissionsServiceProvider = permissionsServiceProvider

    def doFilter(self, request, response, chain):

        wrappedResponse = ResponseWrapper(response)

        chain.doFilter(request, wrappedResponse)

        bytes = wrappedResponse.getCapture()
        if bytes is not None:
            if wrappedResponse.getContentType() is not None and wrappedResponse.getContentType().contains("text/html") or (request).getPathInfo().endsWith("manifest.json"):

                server = None
                try:
                    server = self._permissionsServiceProvider.get().getServer()
                except StorageException as e:
                    raise Exception(e)

                title = server.getString("title", "Traccar")
                description = server.getString("description", "Traccar GPS Tracking System")
                colorPrimary = server.getString("colorPrimary",

                alteredContent = (str(wrappedResponse.getCapture())).replace("${title}", title).replace("${description}", description).replace("${colorPrimary}", self.colorPrimary))

                response.setContentLength(len(self.alteredContent))
                response.getOutputStream().write(self.lteredContent.getBytes())

            else:
                response.getOutputStream().write(bytes)
