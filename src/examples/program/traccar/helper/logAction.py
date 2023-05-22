class LogAction:

    _LOGGER = "LoggerFactory.getLogger(LogAction.class)"

    def __init__(self):
        pass

    _ACTION_CREATE = "create"
    _ACTION_EDIT = "edit"
    _ACTION_REMOVE = "remove"

    _ACTION_LINK = "link"
    _ACTION_UNLINK = "unlink"

    _ACTION_LOGIN = "login"
    _ACTION_LOGOUT = "logout"

    _ACTION_DEVICE_ACCUMULATORS = "resetDeviceAccumulators"

    _PATTERN_OBJECT = "user: %d, action: %s, object: %s, id: %d"
    _PATTERN_LINK = "user: %d, action: %s, owner: %s, id: %d, property: %s, id: %d"
    _PATTERN_LOGIN = "user: %d, action: %s, from: %s"
    _PATTERN_LOGIN_FAILED = "login failed from: %s"
    _PATTERN_DEVICE_ACCUMULATORS = "user: %d, action: %s, deviceId: %d"
    _PATTERN_REPORT = "user: %d, report: %s, from: %s, to: %s, devices: %s, groups: %s"

    @staticmethod
    def create(userId, object):
        LogAction._logObjectAction(LogAction._ACTION_CREATE, userId, type(object), object.getId())

    @staticmethod
    def edit(userId, object):
        LogAction._logObjectAction(LogAction._ACTION_EDIT, userId, type(object), object.getId())

    @staticmethod
    def remove(userId, clazz, objectId):
        LogAction._logObjectAction(LogAction._ACTION_REMOVE, userId, clazz, objectId)

    @staticmethod
    def link(userId, owner, ownerId, property, propertyId):
        LogAction._logLinkAction(LogAction._ACTION_LINK, userId, owner, ownerId, property, propertyId)

    @staticmethod
    def unlink(userId, owner, ownerId, property, propertyId):
        LogAction._logLinkAction(LogAction._ACTION_UNLINK, userId, owner, ownerId, property, propertyId)

    @staticmethod
    def login(userId, remoteAddress):
        LogAction._logLoginAction(LogAction._ACTION_LOGIN, userId, remoteAddress)

    @staticmethod
    def logout(userId, remoteAddress):
        LogAction._logLoginAction(LogAction._ACTION_LOGOUT, userId, remoteAddress)

    @staticmethod
    def failedLogin(remoteAddress):
        if remoteAddress is None or not remoteAddress:
            remoteAddress = "unknown"
        LogAction._LOGGER.info(str.format(LogAction._PATTERN_LOGIN_FAILED, remoteAddress))

    @staticmethod
    def resetDeviceAccumulators(userId, deviceId):
        LogAction._LOGGER.info(str.format(LogAction._PATTERN_DEVICE_ACCUMULATORS, userId, LogAction._ACTION_DEVICE_ACCUMULATORS, deviceId))

    @staticmethod
    def _logObjectAction(action, userId, clazz, objectId):
        LogAction._LOGGER.info(str.format(LogAction._PATTERN_OBJECT, userId, action, (clazz.getSimpleName()).lower(), objectId))

    @staticmethod
    def _logLinkAction(action, userId, owner, ownerId, property, propertyId):
        LogAction._LOGGER.info(str.format(LogAction._PATTERN_LINK, userId, action, (owner.getSimpleName()).lower(), ownerId, (property.getSimpleName()).lower(), propertyId))

    @staticmethod
    def _logLoginAction(action, userId, remoteAddress):
        if remoteAddress is None or not remoteAddress:
            remoteAddress = "unknown"
        LogAction._LOGGER.info(str.format(LogAction._PATTERN_LOGIN, userId, action, remoteAddress))

    @staticmethod
    def logReport(userId, report, from_, to, deviceIds, groupIds):
        dateFormat = format("yyyy-MM-dd HH:mm")
        LogAction._LOGGER.info(str.format(LogAction._PATTERN_REPORT, userId, report, dateFormat.format(from_), dateFormat.format(to), str(deviceIds), str(groupIds)))
