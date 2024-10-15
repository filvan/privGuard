from datetime import date
from mailbox import Message

from pandas.core.indexes.accessors import Properties
from requests import Session

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.configKey import ConfigKey
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.database.statisticManager import StatisticsManager
from src.examples.program.traccar.notification.propertiesProvider import PropertiesProvider
from .mailManager import MailManager


class SmtpMailManager(MailManager):
    _CONTENT_TYPE = "text/html; charset=utf-8"

    def __init__(self, config, statisticsManager):
        # instance fields found by Java to Python Converter:
        self._config = None
        self._statisticsManager = None

        self._config = config
        self._statisticsManager = statisticsManager

    @staticmethod
    def _copyBooleanProperty(properties, provider, key):
        value = provider.getBoolean(key)
        if value is not None:
            properties.put(key.getKey(), str(value))

    @staticmethod
    def _copyStringProperty(properties, provider, key):
        value = provider.getString(key)
        if value is not None:
            properties.put(key.getKey(), value)

    @staticmethod
    def _getProperties(provider):
        host = provider.getString(Keys.MAIL_SMTP_HOST)
        if host is not None:
            properties = Properties()

            properties.put(Keys.MAIL_TRANSPORT_PROTOCOL.getKey(), provider.getString(Keys.MAIL_TRANSPORT_PROTOCOL))
            properties.put(Keys.MAIL_SMTP_HOST.getKey(), host)
            properties.put(Keys.MAIL_SMTP_PORT.getKey(), str(provider.getInteger(Keys.MAIL_SMTP_PORT)))

            SmtpMailManager._copyBooleanProperty(properties, provider, Keys.MAIL_SMTP_STARTTLS_ENABLE)
            SmtpMailManager._copyBooleanProperty(properties, provider, Keys.MAIL_SMTP_STARTTLS_REQUIRED)
            SmtpMailManager._copyBooleanProperty(properties, provider, Keys.MAIL_SMTP_SSL_ENABLE)
            SmtpMailManager._copyStringProperty(properties, provider, Keys.MAIL_SMTP_SSL_TRUST)
            SmtpMailManager._copyStringProperty(properties, provider, Keys.MAIL_SMTP_SSL_PROTOCOLS)
            SmtpMailManager._copyStringProperty(properties, provider, Keys.MAIL_SMTP_USERNAME)
            SmtpMailManager._copyStringProperty(properties, provider, Keys.MAIL_SMTP_PASSWORD)
            SmtpMailManager._copyStringProperty(properties, provider, Keys.MAIL_SMTP_FROM)
            SmtpMailManager._copyStringProperty(properties, provider, Keys.MAIL_SMTP_FROM_NAME)

            return properties
        return None

    def getEmailEnabled(self):
        return self._config.hasKey(Keys.MAIL_SMTP_HOST)

    # JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
    # ORIGINAL LINE: @Override public void sendMessage(User user, boolean system, String subject, String body) throws MessagingException
    # JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def sendMessage(self, user, system, subject, body):
        self.sendMessage(user, system, subject, body, None)

    # JAVA TO PYTHON CONVERTER WARNING: Method 'throws' clauses are not available in Python:
    # ORIGINAL LINE: @Override public void sendMessage(User user, boolean system, String subject, String body, MimeBodyPart attachment) throws MessagingException
    # JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def sendMessage(self, user, system, subject, body, attachment):

        properties = None
        if not self._config.getBoolean(Keys.MAIL_SMTP_IGNORE_USER_CONFIG):
            properties = SmtpMailManager._getProperties(PropertiesProvider(user))
        if properties is None and (system or (not self._config.getBoolean(Keys.MAIL_SMTP_SYSTEM_ONLY))):
            properties = SmtpMailManager._getProperties(PropertiesProvider(self._config))
        if properties is None:
            raise Exception("No SMTP configuration found")

        session = Session.getInstance(properties)

        message = "MimeMessage(session)"

        from_ = properties.getProperty(Keys.MAIL_SMTP_FROM.getKey())
        if from_ is not None:
            fromName = properties.getProperty(Keys.MAIL_SMTP_FROM_NAME.getKey())
            if fromName is not None:
                try:
                    message.setFrom("InternetAddress(from_, fromName)")
                except Exception as e:
                    raise Exception("Email address issue")
            else:
                message.setFrom("InternetAddress(from_)")

        message.addRecipient(Message.RecipientType.TO, "InternetAddress(user.getEmail())")
        message.setSubject(subject)
        message.setSentDate(date())

        if attachment is not None:
            multipart = "MimeMultipart()"

            messageBodyPart = "MimeBodyPart()"
            messageBodyPart.setContent(body, SmtpMailManager._CONTENT_TYPE)
            multipart.addBodyPart(messageBodyPart)
            multipart.addBodyPart(attachment)

            message.setContent(multipart)
        else:
            message.setContent(body, SmtpMailManager._CONTENT_TYPE)

        with session.getTransport() as transport:
            self._statisticsManager.registerMail()
            transport.connect(properties.getProperty(Keys.MAIL_SMTP_HOST.getKey()),
                              properties.getProperty(Keys.MAIL_SMTP_USERNAME.getKey()),
                              properties.getProperty(Keys.MAIL_SMTP_PASSWORD.getKey()))
            transport.sendMessage(message, message.getAllRecipients())
