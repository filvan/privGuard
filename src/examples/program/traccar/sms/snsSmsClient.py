from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.sms.smsManager import SmsManager


class SnsSmsClient(SmsManager):
    _LOGGER = "LoggerFactory.getLogger(SnsSmsClient.class)"


    def __init__(self, config):
        self._snsClient = None

        awsCredentials = "BasicAWSCredentials(config.getString(Keys.SMS_AWS_ACCESS), config.getString(Keys.SMS_AWS_SECRET))"
        self._snsClient = "AmazonSNSAsyncClientBuilder.standard().withRegion(config.getString(Keys.SMS_AWS_REGION)).withCredentials(AWSStaticCredentialsProvider(awsCredentials)).build()"

    def sendMessage(self, destAddress, message, command):
        smsAttributes = {}
        smsAttributes["AWS.SNS.SMS.SenderID"] = ("MessageAttributeValue()").withStringValue("SNS").withDataType("String")
        smsAttributes["AWS.SNS.SMS.SMSType"] = ("MessageAttributeValue()").withStringValue("Transactional").withDataType("String")

        publishRequest = (self.PublishRequest()).withMessage(message).withPhoneNumber(destAddress).withMessageAttributes(smsAttributes)

        self._snsClient.publishAsync(publishRequest, self.AsyncHandlerAnonymousInnerClass(self))

    class AsyncHandlerAnonymousInnerClass():

        def __init__(self, outerInstance):
            self._outerInstance = outerInstance

        def onError(self, exception):
            SnsSmsClient._LOGGER.error("SMS send failed", exception)

        def onSuccess(self, request, result):
            pass
