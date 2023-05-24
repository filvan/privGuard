import os
from calendar import Calendar

from src.examples.program.traccar.api.security.permissionService import PermissionsService
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.helper.unitsConverter import UnitsConverter
from src.examples.program.traccar.helper.model.deviceUtil import DeviceUtil
from src.examples.program.traccar.helper.model.positionUtil import PositionUtil
from src.examples.program.traccar.helper.model.userUtil import UserUtil
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.reports.common.reportUtils import ReportUtils
from src.examples.program.traccar.reports.model.summaryReportItem import SummaryReportItem
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException

class SummaryReportProvider:


    def __init__(self, config, reportUtils, permissionsService, storage):

        self._config = None
        self._reportUtils = None
        self._permissionsService = None
        self._storage = None

        self._config = config
        self._reportUtils = reportUtils
        self._permissionsService = permissionsService
        self._storage = storage

    def _calculateSummaryResult(self, device, positions):
        result = SummaryReportItem()
        result.setDeviceId(device.getId())
        result.setDeviceName(device.getName())
        if positions is not None and positions:
            firstPosition = None
            previousPosition = None
            for position in positions:
                if firstPosition is None:
                    firstPosition = position
                previousPosition = position
                if position.getSpeed() > result.getMaxSpeed():
                    result.setMaxSpeed(position.getSpeed())
            ignoreOdometer = self._config.getBoolean(Keys.REPORT_IGNORE_ODOMETER)
            result.setDistance(PositionUtil.calculateDistance(firstPosition, previousPosition, (not ignoreOdometer)))
            result.setSpentFuel(self._reportUtils.calculateFuel(firstPosition, previousPosition))

            durationMilliseconds = 0
            if firstPosition.hasAttribute(Position.KEY_HOURS) and previousPosition.hasAttribute(Position.KEY_HOURS):
                durationMilliseconds = previousPosition.getLong(Position.KEY_HOURS) - firstPosition.getLong(Position.KEY_HOURS)
                result.setEngineHours(durationMilliseconds)
            else:
                durationMilliseconds = previousPosition.getFixTime().getTime() - firstPosition.getFixTime().getTime()

            if durationMilliseconds > 0:
                result.setAverageSpeed(UnitsConverter.knotsFromMps(result.getDistance() * 1000 / durationMilliseconds))

            if (not ignoreOdometer) and firstPosition.getDouble(Position.KEY_ODOMETER) != 0 and previousPosition.getDouble(Position.KEY_ODOMETER) != 0:
                result.setStartOdometer(firstPosition.getDouble(Position.KEY_ODOMETER))
                result.setEndOdometer(previousPosition.getDouble(Position.KEY_ODOMETER))
            else:
                result.setStartOdometer(firstPosition.getDouble(Position.KEY_TOTAL_DISTANCE))
                result.setEndOdometer(previousPosition.getDouble(Position.KEY_TOTAL_DISTANCE))

            result.setStartTime(firstPosition.getFixTime())
            result.setEndTime(previousPosition.getFixTime())
        return result

    def _getDay(self, userId, date):
        calendar = Calendar.getInstance(UserUtil.getTimezone(self._permissionsService.getServer(), self._permissionsService.getUser(userId)))
        calendar = date
        return calendar.day

    def _calculateSummaryResults(self, userId, device, from_, to, daily):

        positions = PositionUtil.getPositions(self._storage, device.getId(), from_, to)
        results = []
        if daily and not positions.isEmpty():
            startIndex = 0
            startDay = self._getDay(userId, positions.iterator().next().getFixTime())
            for i, unusedItem in enumerate(positions):
                currentDay = self._getDay(userId, positions.get(i).getFixTime())
                if currentDay != startDay:
                    results.append(self._calculateSummaryResult(device, positions.subList(startIndex, i)))
                    startIndex = i
                    startDay = currentDay
            results.append(self._calculateSummaryResult(device, positions.subList(startIndex, positions.size())))
        else:
            results.append(self._calculateSummaryResult(device, positions))

        return results

    def getObjects(self, userId, deviceIds, groupIds, from_, to, daily):
        self._reportUtils.checkPeriodLimit(from_, to)

        result = []
        for device in DeviceUtil.getAccessibleDevices(self._storage, userId, deviceIds, groupIds):
            deviceResults = self._calculateSummaryResults(userId, device, from_, to, daily)
            for summaryReport in deviceResults:
                if summaryReport.getStartTime() is not None and summaryReport.getEndTime() is not None:
                    result.append(summaryReport)
        return result

    def getExcel(self, outputStream, userId, deviceIds, groupIds, from_, to, daily):
        summaries = self.getObjects(userId, deviceIds, groupIds, from_, to, daily)

        file = os.path.get(self._config.getString(Keys.TEMPLATES_ROOT), "export", "summary.xlsx").toFile()
        with "FileInputStream(file)" as inputStream:
            context = self._reportUtils.initializeContext(userId)
            context.putVar("summaries", summaries)
            context.putVar("from", from_)
            context.putVar("to", to)
            "JxlsHelper.getInstance().setUseFastFormulaProcessor(False).processTemplate(inputStream, outputStream, context)"
