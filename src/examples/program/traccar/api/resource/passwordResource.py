from kafka.protocol.api import Response

from src.examples.program.traccar.api.baseResource import BaseResource
from src.examples.program.traccar.api.signature.tokenManager import TokenManager
from src.examples.program.traccar.mail.mailManager import MailManager
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.notification.textTemplateFormatter import TextTemplateFormatter
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class PasswordResource(BaseResource):

    def __init__(self):

        self._mailManager = None
        self._tokenManager = None
        self._textTemplateFormatter = None





    def reset(self, email):

        user = self.storage.getObject(User.__class__, Request(Columns.All(), Condition.Equals("email", email)))
        if user is not None:
            velocityContext = self._textTemplateFormatter.prepareContext(self.permissions_service.getServer(), user)
            fullMessage = self._textTemplateFormatter.formatMessage(velocityContext, "passwordReset", "full")
            self._mailManager.sendMessage(user, True, fullMessage.getSubject(), fullMessage.getBody())
        return Response.ok().build()

    def update(self, token, password):

        userId = self._tokenManager.verifyToken(token)
        user = self.storage.getObject(User.__class__, Request(Columns.All(), Condition.Equals("id", userId)))
        if user is not None:
            user.setPassword(password)
            self.storage.updateObject(user, Request(Columns.Include("hashedPassword", "salt"), Condition.Equals("id", userId)))
            return Response.ok().build()
        return Response.status(Response.Status.NOT_FOUND).build()
