from array import *
from .keyType import KeyType
class Keys:

    def __init__(self):
        pass

    PROTOCOL_ADDRESS = StringConfigSuffix(".address", array(KeyType.CONFIG))

    PROTOCOL_PORT = IntegerConfigSuffix(".port", array(KeyType.CONFIG))

    PROTOCOL_DEVICES = StringConfigSuffix(".devices", array(KeyType.CONFIG))

    PROTOCOL_INTERVAL = LongConfigSuffix(".interval", array(KeyType.CONFIG))

    PROTOCOL_SSL = BooleanConfigSuffix(".ssl", array(KeyType.CONFIG))

    PROTOCOL_TIMEOUT = IntegerConfigSuffix(".timeout", array(KeyType.CONFIG))

    DEVICE_PASSWORD = StringConfigKey("devicePassword", array(KeyType.DEVICE))

    PROTOCOL_DEVICE_PASSWORD = StringConfigSuffix(".devicePassword", array(KeyType.CONFIG))

    PROTOCOL_MASK = IntegerConfigSuffix(".mask", array(KeyType.CONFIG))

    PROTOCOL_MESSAGE_LENGTH = IntegerConfigSuffix(".messageLength", array(KeyType.CONFIG))

    PROTOCOL_EXTENDED = BooleanConfigSuffix(".extended", array(KeyType.CONFIG))

    PROTOCOL_UTF8 = BooleanConfigSuffix(".utf8", array(KeyType.CONFIG))

    PROTOCOL_CAN = BooleanConfigSuffix(".can", array(KeyType.CONFIG))

    PROTOCOL_ACK = BooleanConfigSuffix(".ack", array(KeyType.CONFIG, KeyType.DEVICE), False)

    PROTOCOL_IGNORE_FIX_TIME = BooleanConfigSuffix(".ignoreFixTime", array(KeyType.CONFIG))

    PROTOCOL_DECODE_LOW = BooleanConfigSuffix(".decodeLow", array(KeyType.CONFIG))

    PROTOCOL_LONG_DATE = BooleanConfigSuffix(".longDate", array(KeyType.CONFIG))

    PROTOCOL_DECIMAL_FUEL = BooleanConfigSuffix(".decimalFuel", array(KeyType.CONFIG))

    PROTOCOL_CUSTOM = BooleanConfigSuffix(".custom", array(KeyType.CONFIG))

    PROTOCOL_FORM = StringConfigSuffix(".form", array(KeyType.CONFIG))

    PROTOCOL_CONFIG = StringConfigSuffix(".config", array(KeyType.CONFIG))

    PROTOCOL_ALARM_MAP = StringConfigSuffix(".alarmMap", array(KeyType.CONFIG))

    PROTOCOL_PREFIX = BooleanConfigSuffix(".prefix", array(KeyType.CONFIG))

    PROTOCOL_SERVER = StringConfigSuffix(".server", array(KeyType.CONFIG))

    PROTOCOL_TYPE = IntegerConfigKey("suntech.protocolType", array(KeyType.CONFIG, KeyType.DEVICE))

    PROTOCOL_HBM = BooleanConfigKey("suntech.hbm", array(KeyType.CONFIG, KeyType.DEVICE))

    PROTOCOL_INCLUDE_ADC = BooleanConfigSuffix(".includeAdc", array(KeyType.CONFIG, KeyType.DEVICE))

    PROTOCOL_INCLUDE_RPM = BooleanConfigSuffix(".includeRpm", array(KeyType.CONFIG, KeyType.DEVICE))

    PROTOCOL_INCLUDE_TEMPERATURE = BooleanConfigSuffix(".includeTemp", array(KeyType.CONFIG, KeyType.DEVICE))

    PROTOCOL_FORMAT = StringConfigSuffix(".format", array(KeyType.DEVICE))

    PROTOCOL_DATE_FORMAT = StringConfigSuffix(".dateFormat", array(KeyType.DEVICE))

    DECODER_TIMEZONE = StringConfigKey("decoder.timezone", array(KeyType.CONFIG, KeyType.DEVICE))

    ORBCOMM_ACCESS_ID = StringConfigKey("orbcomm.accessId", array(KeyType.CONFIG))

    ORBCOMM_PASSWORD = StringConfigKey("orbcomm.password", array(KeyType.CONFIG))

    PROTOCOL_ALTERNATIVE = BooleanConfigSuffix(".alternative", array(KeyType.CONFIG, KeyType.DEVICE), False)

    PROTOCOL_LANGUAGE = BooleanConfigSuffix(".language", array(KeyType.CONFIG, KeyType.DEVICE), False)

    SERVER_TIMEOUT = IntegerConfigKey("server.timeout", array(KeyType.CONFIG))

    SERVER_INSTANT_ACKNOWLEDGEMENT = BooleanConfigKey("server.instantAcknowledgement", array(KeyType.CONFIG))

    SERVER_STATISTICS = StringConfigKey("server.statistics", array(KeyType.CONFIG))

    EVENT_FUEL_DROP_THRESHOLD = DoubleConfigKey("fuelDropThreshold", array(KeyType.SERVER, KeyType.DEVICE), 0.0)

    EVENT_FUEL_INCREASE_THRESHOLD = DoubleConfigKey("fuelIncreaseThreshold", array(KeyType.SERVER, KeyType.DEVICE), 0.0)

    EVENT_OVERSPEED_LIMIT = DoubleConfigKey("speedLimit", array(KeyType.SERVER, KeyType.DEVICE), 0.0)

    EVENT_OVERSPEED_MINIMAL_DURATION = LongConfigKey("event.overspeed.minimalDuration", array(KeyType.CONFIG))

    EVENT_OVERSPEED_PREFER_LOWEST = BooleanConfigKey("event.overspeed.preferLowest", array(KeyType.CONFIG))

    EVENT_BEHAVIOR_ACCELERATION_THRESHOLD = DoubleConfigKey("event.behavior.accelerationThreshold", array(KeyType.CONFIG))

    EVENT_BEHAVIOR_BRAKING_THRESHOLD = DoubleConfigKey("event.behavior.brakingThreshold", array(KeyType.CONFIG))

    EVENT_IGNORE_DUPLICATE_ALERTS = BooleanConfigKey("event.ignoreDuplicateAlerts", array(KeyType.CONFIG))

    EVENT_MOTION_PROCESS_INVALID_POSITIONS = BooleanConfigKey("event.motion.processInvalidPositions", array(KeyType.CONFIG, KeyType.DEVICE), False)

    EVENT_MOTION_SPEED_THRESHOLD = DoubleConfigKey("event.motion.speedThreshold", array(KeyType.CONFIG, KeyType.DEVICE), 0.01)

    GEOFENCE_POLYLINE_DISTANCE = DoubleConfigKey("geofence.polylineDistance", array(KeyType.CONFIG), 25.0)
    DATABASE_MEMORY = BooleanConfigKey("database.memory", array(KeyType.CONFIG))

    DATABASE_DRIVER_FILE = StringConfigKey("database.driverFile", array(KeyType.CONFIG))

    DATABASE_DRIVER = StringConfigKey("database.driver", array(KeyType.CONFIG))

    DATABASE_URL = StringConfigKey("database.url", array(KeyType.CONFIG))

    DATABASE_USER = StringConfigKey("database.user", array(KeyType.CONFIG))

    DATABASE_PASSWORD = StringConfigKey("database.password", array(KeyType.CONFIG))

    DATABASE_CHANGELOG = StringConfigKey("database.changelog", array(KeyType.CONFIG))

    DATABASE_MAX_POOL_SIZE = IntegerConfigKey("database.maxPoolSize", array(KeyType.CONFIG))

    DATABASE_CHECK_CONNECTION = StringConfigKey("database.checkConnection", array(KeyType.CONFIG), "SELECT 1")
    DATABASE_SAVE_ORIGINAL = BooleanConfigKey("database.saveOriginal", array(KeyType.CONFIG))

    DATABASE_THROTTLE_UNKNOWN = BooleanConfigKey("database.throttleUnknown", array(KeyType.CONFIG))

    DATABASE_IGNORE_UNKNOWN = BooleanConfigKey("database.ignoreUnknown", array(KeyType.CONFIG))

    DATABASE_REGISTER_UNKNOWN = BooleanConfigKey("database.registerUnknown", array(KeyType.CONFIG))

    DATABASE_REGISTER_UNKNOWN_DEFAULT_CATEGORY = StringConfigKey("database.registerUnknown.defaultCategory",
                                                                 array(KeyType.CONFIG))

    DATABASE_REGISTER_UNKNOWN_DEFAULT_GROUP_ID = LongConfigKey("database.registerUnknown.defaultGroupId",
                                                               array(KeyType.CONFIG))

    DATABASE_REGISTER_UNKNOWN_REGEX = StringConfigKey("database.registerUnknown.regex", array(KeyType.CONFIG),
                                                      "\\w{3,15}")

    DATABASE_SAVE_EMPTY = BooleanConfigKey("database.saveEmpty", array(KeyType.CONFIG))

    USERS_DEFAULT_DEVICE_LIMIT = IntegerConfigKey("users.defaultDeviceLimit", array(KeyType.CONFIG), -1)

    USERS_DEFAULT_EXPIRATION_DAYS = IntegerConfigKey("users.defaultExpirationDays", array(KeyType.CONFIG))

    LDAP_URL = StringConfigKey("ldap.url", array(KeyType.CONFIG))

    LDAP_USER = StringConfigKey("ldap.user", array(KeyType.CONFIG))

    LDAP_PASSWORD = StringConfigKey("ldap.password", array(KeyType.CONFIG))

    LDAP_FORCE = BooleanConfigKey("ldap.force", array(KeyType.CONFIG))

    LDAP_BASE = StringConfigKey("ldap.base", array(KeyType.CONFIG))

    LDAP_ID_ATTRIBUTE = StringConfigKey("ldap.idAttribute", array(KeyType.CONFIG), "uid")

    LDAP_NAME_ATTRIBUTE = StringConfigKey("ldap.nameAttribute", array(KeyType.CONFIG), "cn")

    LDAP_MAIN_ATTRIBUTE = StringConfigKey("ldap.mailAttribute", array(KeyType.CONFIG), "mail")

    LDAP_SEARCH_FILTER = StringConfigKey("ldap.searchFilter", array(KeyType.CONFIG))

    LDAP_ADMIN_FILTER = StringConfigKey("ldap.adminFilter", array(KeyType.CONFIG))

    LDAP_ADMIN_GROUP = StringConfigKey("ldap.adminGroup", array(KeyType.CONFIG))

    OPENID_FORCE = BooleanConfigKey("openid.force", array(KeyType.CONFIG))

    OPENID_CLIENT_ID = StringConfigKey("openid.clientId", array(KeyType.CONFIG))

    OPENID_CLIENT_SECRET = StringConfigKey("openid.clientSecret", array(KeyType.CONFIG))

    OPENID_ISSUER_URL = StringConfigKey("openid.issuerUrl", array(KeyType.CONFIG))
    OPENID_AUTH_URL = StringConfigKey("openid.authUrl", array(KeyType.CONFIG))
    OPENID_TOKEN_URL = StringConfigKey("openid.tokenUrl", array(KeyType.CONFIG))

    OPENID_USERINFO_URL = StringConfigKey("openid.userInfoUrl", array(KeyType.CONFIG))

    OPENID_ALLOW_GROUP = StringConfigKey("openid.allowGroup", array(KeyType.CONFIG))

    OPENID_ADMIN_GROUP = StringConfigKey("openid.adminGroup", array(KeyType.CONFIG))

    STATUS_TIMEOUT = LongConfigKey("status.timeout", array(KeyType.CONFIG), 600)

    STATUS_IGNORE_OFFLINE = StringConfigKey("status.ignoreOffline", array(KeyType.CONFIG))
    MEDIA_PATH = StringConfigKey("media.path", array(KeyType.CONFIG))

    WEB_ADDRESS = StringConfigKey("web.address", array(KeyType.CONFIG))

    WEB_PORT = IntegerConfigKey("web.port", array(KeyType.CONFIG))

    WEB_MAX_REQUESTS_PER_SECOND = IntegerConfigKey("web.maxRequestsPerSec", array(KeyType.CONFIG))

    WEB_SANITIZE = BooleanConfigKey("web.sanitize", array(KeyType.CONFIG))

    WEB_PATH = StringConfigKey("web.path", array(KeyType.CONFIG))

    WEB_OVERRIDE = StringConfigKey("web.override", array(KeyType.CONFIG))

    WEB_TIMEOUT = LongConfigKey("web.timeout", array(KeyType.CONFIG), 60000)

    WEB_SESSION_TIMEOUT = IntegerConfigKey("web.sessionTimeout", array(KeyType.CONFIG))

    WEB_CONSOLE = BooleanConfigKey("web.console", array(KeyType.CONFIG))

    WEB_DEBUG = BooleanConfigKey("web.debug", array(KeyType.CONFIG))

    WEB_SERVICE_ACCOUNT_TOKEN = StringConfigKey("web.serviceAccountToken", array(KeyType.CONFIG))

    WEB_ORIGIN = StringConfigKey("web.origin", array(KeyType.CONFIG))

    WEB_CACHE_CONTROL = StringConfigKey("web.cacheControl", array(KeyType.CONFIG), "max-age=3600,public")

    SERVER_FORWARD = StringConfigKey("server.forward", array(KeyType.CONFIG))

    FORWARD_TYPE = StringConfigKey("forward.type", array(KeyType.CONFIG), "url")

    FORWARD_TOPIC = StringConfigKey("forward.topic", array(KeyType.CONFIG), "positions")

    FORWARD_URL = StringConfigKey("forward.url", array(KeyType.CONFIG))

    FORWARD_HEADER = StringConfigKey("forward.header", array(KeyType.CONFIG))
    FORWARD_RETRY_ENABLE = BooleanConfigKey("forward.retry.enable", array(KeyType.CONFIG))
    FORWARD_RETRY_DELAY = IntegerConfigKey("forward.retry.delay", array(KeyType.CONFIG), 100)
    FORWARD_RETRY_COUNT = IntegerConfigKey("forward.retry.count", array(KeyType.CONFIG), 10)
    FORWARD_RETRY_LIMIT = IntegerConfigKey("forward.retry.limit", array(KeyType.CONFIG), 100)
    EVENT_FORWARD_TYPE = StringConfigKey("event.forward.type", array(KeyType.CONFIG), "json")

    EVENT_FORWARD_TOPIC = StringConfigKey("event.forward.topic", array(KeyType.CONFIG), "events")

    EVENT_FORWARD_URL = StringConfigKey("event.forward.url", array(KeyType.CONFIG))

    EVENT_FORWARD_HEADERS = StringConfigKey("event.forward.header", array(KeyType.CONFIG))

    TEMPLATES_ROOT = StringConfigKey("templates.root", array(KeyType.CONFIG), "templates")

    MAIL_DEBUG = BooleanConfigKey("mail.debug", array(KeyType.CONFIG))

    MAIL_SMTP_SYSTEM_ONLY = BooleanConfigKey("mail.smtp.systemOnly", array(KeyType.CONFIG))

    MAIL_SMTP_IGNORE_USER_CONFIG = BooleanConfigKey("mail.smtp.ignoreUserConfig", array(KeyType.CONFIG))

    MAIL_SMTP_HOST = StringConfigKey("mail.smtp.host", array(KeyType.CONFIG, KeyType.USER))
    MAIL_SMTP_PORT = IntegerConfigKey("mail.smtp.port", array(KeyType.CONFIG, KeyType.USER), 25)
    MAIL_TRANSPORT_PROTOCOL = StringConfigKey("mail.transport.protocol", array(KeyType.CONFIG, KeyType.USER), "smtp")

    MAIL_SMTP_STARTTLS_ENABLE = BooleanConfigKey("mail.smtp.starttls.enable", array(KeyType.CONFIG, KeyType.USER))

    MAIL_SMTP_STARTTLS_REQUIRED = BooleanConfigKey("mail.smtp.starttls.required", array(KeyType.CONFIG, KeyType.USER))

    MAIL_SMTP_SSL_ENABLE = BooleanConfigKey("mail.smtp.ssl.enable", array(KeyType.CONFIG, KeyType.USER))
    MAIL_SMTP_SSL_TRUST = StringConfigKey("mail.smtp.ssl.trust", array(KeyType.CONFIG, KeyType.USER))

    MAIL_SMTP_SSL_PROTOCOLS = StringConfigKey("mail.smtp.ssl.protocols", array(KeyType.CONFIG, KeyType.USER))

    MAIL_SMTP_USERNAME = StringConfigKey("mail.smtp.username", array(KeyType.CONFIG, KeyType.USER))

    MAIL_SMTP_PASSWORD = StringConfigKey("mail.smtp.password", array(KeyType.CONFIG, KeyType.USER))

    MAIL_SMTP_FROM = StringConfigKey("mail.smtp.from", array(KeyType.CONFIG, KeyType.USER))

    MAIL_SMTP_FROM_NAME = StringConfigKey("mail.smtp.fromName", array(KeyType.CONFIG, KeyType.USER))

    SMS_HTTP_URL = StringConfigKey("sms.http.url", array(KeyType.CONFIG))

    SMS_HTTP_AUTHORIZATION_HEADER = StringConfigKey("sms.http.authorizationHeader", array(KeyType.CONFIG),
                                                    "Authorization")

    SMS_HTTP_AUTHORIZATION = StringConfigKey("sms.http.authorization", array(KeyType.CONFIG))

    SMS_HTTP_USER = StringConfigKey("sms.http.user", array(KeyType.CONFIG))

    SMS_HTTP_PASSWORD = StringConfigKey("sms.http.password", array(KeyType.CONFIG))
    SMS_HTTP_TEMPLATE = StringConfigKey("sms.http.template", array(KeyType.CONFIG))

    SMS_AWS_ACCESS = StringConfigKey("sms.aws.access", array(KeyType.CONFIG))

    SMS_AWS_SECRET = StringConfigKey("sms.aws.secret", array(KeyType.CONFIG))

    SMS_AWS_REGION = StringConfigKey("sms.aws.region", array(KeyType.CONFIG))

    NOTIFICATOR_TYPES = StringConfigKey("notificator.types", array(KeyType.CONFIG))

    NOTIFICATOR_TRACCAR_KEY = StringConfigKey("notificator.traccar.key", array(KeyType.CONFIG))

    NOTIFICATOR_FIREBASE_SERVICE_ACCOUNT = StringConfigKey("notificator.firebase.serviceAccount",
                                                           array(KeyType.CONFIG))

    NOTIFICATOR_PUSHOVER_USER = StringConfigKey("notificator.pushover.user", array(KeyType.CONFIG))

    NOTIFICATOR_PUSHOVER_TOKEN = StringConfigKey("notificator.pushover.token", array(KeyType.CONFIG))

    NOTIFICATOR_TELEGRAM_KEY = StringConfigKey("notificator.telegram.key", array(KeyType.CONFIG))

    NOTIFICATOR_TELEGRAM_CHAT_ID = StringConfigKey("notificator.telegram.chatId", array(KeyType.CONFIG))

    NOTIFICATOR_TELEGRAM_SEND_LOCATION = BooleanConfigKey("notificator.telegram.sendLocation", array(KeyType.CONFIG))

    REPORT_PERIOD_LIMIT = LongConfigKey("report.periodLimit", array(KeyType.CONFIG))
    REPORT_TRIP_MINIMAL_TRIP_DISTANCE = LongConfigKey("report.trip.minimalTripDistance",
                                                      array(KeyType.CONFIG, KeyType.DEVICE), 500)
    REPORT_TRIP_MINIMAL_TRIP_DURATION = LongConfigKey("report.trip.minimalTripDuration",
                                                      array(KeyType.CONFIG, KeyType.DEVICE), 300)
    REPORT_TRIP_MINIMAL_PARKING_DURATION = LongConfigKey("report.trip.minimalParkingDuration",
                                                         array(KeyType.CONFIG, KeyType.DEVICE), 300)

    REPORT_TRIP_MINIMAL_NO_DATA_DURATION = LongConfigKey("report.trip.minimalNoDataDuration",
                                                         array(KeyType.CONFIG, KeyType.DEVICE), 3600)

    REPORT_TRIP_USE_IGNITION = BooleanConfigKey("report.trip.useIgnition", array(KeyType.CONFIG, KeyType.DEVICE),
                                                False)

    REPORT_IGNORE_ODOMETER = BooleanConfigKey("report.ignoreOdometer", array(KeyType.CONFIG), False)

    FILTER_ENABLE = BooleanConfigKey("filter.enable", array(KeyType.CONFIG))

    FILTER_INVALID = BooleanConfigKey("filter.invalid", array(KeyType.CONFIG))

    FILTER_ZERO = BooleanConfigKey("filter.zero", array(KeyType.CONFIG))

    FILTER_DUPLICATE = BooleanConfigKey("filter.duplicate", array(KeyType.CONFIG))

    FILTER_OUTDATED = BooleanConfigKey("filter.outdated", array(KeyType.CONFIG))

    FILTER_FUTURE = LongConfigKey("filter.future", array(KeyType.CONFIG))

    FILTER_PAST = LongConfigKey("filter.past", array(KeyType.CONFIG))

    FILTER_ACCURACY = IntegerConfigKey("filter.accuracy", array(KeyType.CONFIG))

    FILTER_APPROXIMATE = BooleanConfigKey("filter.approximate", array(KeyType.CONFIG))

    FILTER_STATIC = BooleanConfigKey("filter.static", array(KeyType.CONFIG))

    FILTER_DISTANCE = IntegerConfigKey("filter.distance", array(KeyType.CONFIG))
    FILTER_MAX_SPEED = IntegerConfigKey("filter.maxSpeed", array(KeyType.CONFIG))

    FILTER_MIN_PERIOD = IntegerConfigKey("filter.minPeriod", array(KeyType.CONFIG))

    FILTER_RELATIVE = BooleanConfigKey("filter.relative", array(KeyType.CONFIG))

    FILTER_SKIP_LIMIT = LongConfigKey("filter.skipLimit", array(KeyType.CONFIG))

    FILTER_SKIP_ATTRIBUTES_ENABLE = BooleanConfigKey("filter.skipAttributes.enable", array(KeyType.CONFIG))

    FILTER_SKIP_ATTRIBUTES = StringConfigKey("filter.skipAttributes", array(KeyType.CONFIG, KeyType.DEVICE), "")

    TIME_OVERRIDE = StringConfigKey("time.override", array(KeyType.CONFIG))

    PROTOCOLS_ENABLE = StringConfigKey("protocols.enable", array(KeyType.CONFIG))

    TIME_PROTOCOLS = StringConfigKey("time.protocols", array(KeyType.CONFIG))

    COORDINATES_FILTER = BooleanConfigKey("coordinates.filter", array(KeyType.CONFIG))

    COORDINATES_MIN_ERROR = IntegerConfigKey("coordinates.minError", array(KeyType.CONFIG))

    COORDINATES_MAX_ERROR = IntegerConfigKey("coordinates.maxError", array(KeyType.CONFIG))

    PROCESSING_REMOTE_ADDRESS_ENABLE = BooleanConfigKey("processing.remoteAddress.enable", array(KeyType.CONFIG))

    PROCESSING_COPY_ATTRIBUTES_ENABLE = BooleanConfigKey("processing.copyAttributes.enable", array(KeyType.CONFIG))

    PROCESSING_COPY_ATTRIBUTES = StringConfigKey("processing.copyAttributes", array(KeyType.CONFIG, KeyType.DEVICE))
    PROCESSING_COMPUTED_ATTRIBUTES_DEVICE_ATTRIBUTES = BooleanConfigKey(
        "processing.computedAttributes.deviceAttributes", array(KeyType.CONFIG))

    PROCESSING_COMPUTED_ATTRIBUTES_LOCAL_VARIABLES = BooleanConfigKey("processing.computedAttributes.localVariables",
                                                                      array(KeyType.CONFIG))

    PROCESSING_COMPUTED_ATTRIBUTES_LOOPS = BooleanConfigKey("processing.computedAttributes.loops",
                                                            array(KeyType.CONFIG))
    PROCESSING_COMPUTED_ATTRIBUTES_NEW_INSTANCE_CREATION = BooleanConfigKey(
        "processing.computedAttributes.newInstanceCreation", array(KeyType.CONFIG))

    GEOCODER_ENABLE = BooleanConfigKey("geocoder.enable", array(KeyType.CONFIG))

    GEOCODER_TYPE = StringConfigKey("geocoder.type", array(KeyType.CONFIG))

    GEOCODER_URL = StringConfigKey("geocoder.url", array(KeyType.CONFIG))

    GEOCODER_ID = StringConfigKey("geocoder.id", array(KeyType.CONFIG))

    GEOCODER_KEY = StringConfigKey("geocoder.key", array(KeyType.CONFIG))

    GEOCODER_LANGUAGE = StringConfigKey("geocoder.language", array(KeyType.CONFIG))
    GEOCODER_FORMAT = StringConfigKey("geocoder.format", array(KeyType.CONFIG))

    GEOCODER_CACHE_SIZE = IntegerConfigKey("geocoder.cacheSize", array(KeyType.CONFIG))

    GEOCODER_IGNORE_POSITIONS = BooleanConfigKey("geocoder.ignorePositions", array(KeyType.CONFIG))

    GEOCODER_PROCESS_INVALID_POSITIONS = BooleanConfigKey("geocoder.processInvalidPositions", array(KeyType.CONFIG))

    GEOCODER_REUSE_DISTANCE = IntegerConfigKey("geocoder.reuseDistance", array(KeyType.CONFIG))

    GEOCODER_ON_REQUEST = BooleanConfigKey("geocoder.onRequest", array(KeyType.CONFIG))

    GEOLOCATION_ENABLE = BooleanConfigKey("geolocation.enable", array(KeyType.CONFIG))

    GEOLOCATION_TYPE = StringConfigKey("geolocation.type", array(KeyType.CONFIG))

    GEOLOCATION_URL = StringConfigKey("geolocation.url", array(KeyType.CONFIG))

    GEOLOCATION_KEY = StringConfigKey("geolocation.key", array(KeyType.CONFIG))

    GEOLOCATION_PROCESS_INVALID_POSITIONS = BooleanConfigKey("geolocation.processInvalidPositions",
                                                             array(KeyType.CONFIG))

    GEOLOCATION_REUSE = BooleanConfigKey("geolocation.reuse", array(KeyType.CONFIG))

    GEOLOCATION_MCC = IntegerConfigKey("geolocation.mcc", array(KeyType.CONFIG))

    GEOLOCATION_MNC = IntegerConfigKey("geolocation.mnc", array(KeyType.CONFIG))

    SPEED_LIMIT_ENABLE = BooleanConfigKey("speedLimit.enable", array(KeyType.CONFIG))

    SPEED_LIMIT_TYPE = StringConfigKey("speedLimit.type", array(KeyType.CONFIG))

    SPEED_LIMIT_URL = StringConfigKey("speedLimit.url", array(KeyType.CONFIG))
    LOCATION_LATITUDE_HEMISPHERE = StringConfigKey("location.latitudeHemisphere", array(KeyType.CONFIG))
    LOCATION_LONGITUDE_HEMISPHERE = StringConfigKey("location.longitudeHemisphere", array(KeyType.CONFIG))
    WEB_REQUEST_LOG_PATH = StringConfigKey("web.requestLog.path", array(KeyType.CONFIG))

    WEB_REQUEST_LOG_RETAIN_DAYS = IntegerConfigKey("web.requestLog.retainDays", array(KeyType.CONFIG))

    WEB_DISABLE_HEALTH_CHECK = BooleanConfigKey("web.disableHealthCheck", array(KeyType.CONFIG))

    WEB_SAME_SITE_COOKIE = StringConfigKey("web.sameSiteCookie", array(KeyType.CONFIG))

    WEB_PERSIST_SESSION = BooleanConfigKey("web.persistSession", array(KeyType.CONFIG))

    WEB_URL = StringConfigKey("web.url", array(KeyType.CONFIG))

    LOGGER_CONSOLE = BooleanConfigKey("logger.console", array(KeyType.CONFIG))

    LOGGER_QUERIES = BooleanConfigKey("logger.queries", array(KeyType.CONFIG))

    LOGGER_FILE = StringConfigKey("logger.file", array(KeyType.CONFIG))

    LOGGER_LEVEL = StringConfigKey("logger.level", array(KeyType.CONFIG))

    LOGGER_FULL_STACK_TRACES = BooleanConfigKey("logger.fullStackTraces", array(KeyType.CONFIG))

    LOGGER_ROTATE = BooleanConfigKey("logger.rotate", array(KeyType.CONFIG))
    LOGGER_ROTATE_INTERVAL = StringConfigKey("logger.rotate.interval", array(KeyType.CONFIG), "day")

    LOGGER_ATTRIBUTES = StringConfigKey("logger.attributes", array(KeyType.CONFIG),
                                        "time,position,speed,course,accuracy,result")

    BROADCAST_INTERFACE = StringConfigKey("broadcast.interface", array(KeyType.CONFIG))
