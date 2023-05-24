from src.examples.program.traccar.api.security.permissionService import PermissionsService
from src.examples.program.traccar.mail.mailManager import MailManager
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.storage.storageException import StorageException

class ReportMailer:

    _LOGGER = "LoggerFactory.getLogger(ReportMailer.class)"


    def __init__(self, permissionsService, mailManager):
        self._permissionsService = None
        self._mailManager = None

        self._permissionsService = permissionsService
        self._mailManager = mailManager

    def sendAsync(self, userId, executor):
        #JAVA TO PYTHON CONVERTER TASK: Only expression lambdas are converted by Java to Python Converter:
        #        new Thread(() ->
        #        {
        #            try
        #            {
        #                var stream = new ByteArrayOutputStream()
        #                executor.execute(stream)
        #
        #                MimeBodyPart attachment = new MimeBodyPart()
        #                attachment.setFileName("report.xlsx")
        #                attachment.setDataHandler(new DataHandler(new ByteArrayDataSource(stream.toByteArray(), "application/octet-stream")))
        #
        #                User user = permissionsService.getUser(userId)
        #                mailManager.sendMessage(user, false, "Report", "The report is in the attachment.", attachment)
        #            }
        #            catch (StorageException | IOException | MessagingException e)
        #            {
        #                LOGGER.warn("Email report failed", e)
        #            }
        #        }
        #        ).start()
        pass
