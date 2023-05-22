from src.examples.program.traccar.mail.mailManager import MailManager
from src.examples.program.traccar.model.user import User

class LogMailManager(MailManager):

    _LOGGER = "LoggerFactory.getLogger(LogMailManager.class)"

    def getEmailEnabled(self):
        return True


    def sendMessage(self, user, system, subject, body):
        self.sendMessage(user, system, subject, body, None)

    def sendMessage(self, user, system, subject, body, attachment):
        LogMailManager._LOGGER.info("Email sent\nTo: {}\nSubject: {}\nAttachment: {}\nBody:\n{}", user.getEmail(), subject,attachment.getFileName() if attachment is not None else None, body)
