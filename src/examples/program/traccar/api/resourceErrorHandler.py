from kafka.protocol.api import Response

from src.examples.program.traccar.helper.log import Log

class ResourceErrorHandler():

    def toResponse(self, e):
        if isinstance(e, Exception):
            webException = e
            return Response.fromResponse(webException.getResponse()).entity(Log.exceptionStack(webException)).build()
        else:
            return Response.status(Response.Status.BAD_REQUEST).entity(Log.exceptionStack(e)).build()
