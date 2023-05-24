import locale
import numbers
import os
from datetime import date

from src.examples.program.traccar.api.signature.tokenManager import TokenManager
from src.examples.program.traccar.helper.model.userUtil import UserUtil
from src.examples.program.traccar.model.server import Server
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.notification.notificationMessage import NotificationMessage
from src.examples.program.traccar.storage.storageException import StorageException





class TextTemplateFormatter:

    _LOGGER = "LoggerFactory.getLogger(TextTemplateFormatter.class)"


    def __init__(self, velocityEngine, tokenManager):

        self._velocityEngine = None
        self._tokenManager = None

        self._velocityEngine = velocityEngine
        self._tokenManager = tokenManager

    def prepareContext(self, server, user):

        velocityContext = "VelocityContext()"

        if user is not None:
            velocityContext.put("user", user)
            velocityContext.put("timezone", UserUtil.getTimezone(server, user))
            try:
                velocityContext.put("token", self._tokenManager.generateToken(user.getId()))
            except (Exception, StorageException )as e:
                TextTemplateFormatter._LOGGER.warn("Token generation failed", e)

        velocityContext.put("webUrl", self._velocityEngine.getProperty("web.url"))
        velocityContext.put("dateTool", date())
        velocityContext.put("numberTool", numbers.Number)
        velocityContext.put("locale", locale.getDefault())

        return velocityContext

    def getTemplate(self, name, path):

        templateFilePath = None
        template = None

        try:
            templateFilePath = str(os.path.get(path, name + ".vm"))
            template = self._velocityEngine.getTemplate(templateFilePath, "StandardCharsets.UTF_8.name()")
        except Exception as error:
            TextTemplateFormatter._LOGGER.warn("Notification template error", error)
            templateFilePath = str(os.path.get(path, "unknown.vm"))
            template = self._velocityEngine.getTemplate(templateFilePath, "StandardCharsets.UTF_8.name()")
        return template

    def formatMessage(self, velocityContext, name, templatePath):
        writer = ""
        self.getTemplate(name, templatePath).merge(velocityContext, writer)
        return NotificationMessage(str(velocityContext.get("subject")), str(writer))
