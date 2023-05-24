import decimal
import locale
import numbers
from datetime import date

from src.examples.program.traccar.api.security.permissionService import PermissionsService
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.geocoder.geocoder import Geocoder
from src.examples.program.traccar.helper.unitsConverter import UnitsConverter
from src.examples.program.traccar.helper.model.attributeUtil import AttributeUtil
from src.examples.program.traccar.helper.model.positionUtil import PositionUtil
from src.examples.program.traccar.helper.model.userUtil import UserUtil
from src.examples.program.traccar.model.baseModel import BaseModel
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.model.driver import Driver
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.model.user import User
from src.examples.program.traccar.reports.common.tripsConfig import TripsConfig
from src.examples.program.traccar.reports.model.baseReportItem import BaseReportItem
from src.examples.program.traccar.reports.model.stopReportItem import StopReportItem
from src.examples.program.traccar.reports.model.tripReportItem import TripReportItem
from src.examples.program.traccar.session.state.motionProcessor import MotionProcessor
from src.examples.program.traccar.session.state.motionState import MotionState
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request





class ReportUtils:


    def __init__(self, config, storage, permissionsService, velocityEngine, geocoder):

        self._config = None
        self._storage = None
        self._permissionsService = None
        self._velocityEngine = None
        self._geocoder = None

        self._config = config
        self._storage = storage
        self._permissionsService = permissionsService
        self._velocityEngine = velocityEngine
        self._geocoder = geocoder

    def getObject(self, userId, clazz, objectId):
        return self._storage.getObject(clazz, Request(Columns.All(), Condition.And(Condition.Equals("id", objectId), Condition.Permission(User.__class__, userId, clazz))))

    def checkPeriodLimit(self, from_, to):
        limit = self._config.getLong(Keys.REPORT_PERIOD_LIMIT) * 1000
        if limit > 0 and to.getTime() - from_.getTime() > limit:
            raise Exception("Time period exceeds the limit")

    def calculateFuel(self, firstPosition, lastPosition):

        if firstPosition.getAttributes().get(Position.KEY_FUEL_LEVEL) is not None and lastPosition.getAttributes().get(Position.KEY_FUEL_LEVEL) is not None:

            value = decimal.valueOf(firstPosition.getDouble(Position.KEY_FUEL_LEVEL) - lastPosition.getDouble(Position.KEY_FUEL_LEVEL))
            return value.setScale(1, round().HALF_EVEN).doubleValue()
        return 0

    def findDriver(self, firstPosition, lastPosition):
        if firstPosition.hasAttribute(Position.KEY_DRIVER_UNIQUE_ID):
            return firstPosition.getString(Position.KEY_DRIVER_UNIQUE_ID)
        elif lastPosition.hasAttribute(Position.KEY_DRIVER_UNIQUE_ID):
            return lastPosition.getString(Position.KEY_DRIVER_UNIQUE_ID)
        return None

    def findDriverName(self, driverUniqueId):
        if driverUniqueId is not None:
            driver = self._storage.getObject(Driver.__class__, Request(Columns.All(), Condition.Equals("uniqueId", driverUniqueId)))
            if driver is not None:
                return driver.getName()
        return None

    def initializeContext(self, userId):
        server = self._permissionsService.getServer()
        user = self._permissionsService.getUser(userId)
        context = "PoiTransformer.createInitialContext()"
        context.putVar("distanceUnit", UserUtil.getDistanceUnit(server, user))
        context.putVar("speedUnit", UserUtil.getSpeedUnit(server, user))
        context.putVar("volumeUnit", UserUtil.getVolumeUnit(server, user))
        context.putVar("webUrl", self._velocityEngine.getProperty("web.url"))
        context.putVar("dateTool", date())
        context.putVar("numberTool", numbers)
        context.putVar("timezone", UserUtil.getTimezone(server, user))
        context.putVar("locale", locale.getDefault())
        context.putVar("bracketsRegex", "[\\{\\}\"]")
        return context

    def processTemplateWithSheets(self, templateStream, targetStream, context):

        transformer = "TransformerFactory.createTransformer(templateStream, targetStream)"
        xlsAreas = "(XlsCommentAreaBuilder(transformer)).build()"
        for xlsArea in xlsAreas:
            xlsArea.applyAt("CellRef(xlsArea.getStartCellRef().getCellName())", context)
            xlsArea.setFormulaProcessor("StandardFormulaProcessor()")
            xlsArea.processFormulas()
        transformer.deleteSheet(xlsAreas[0].getStartCellRef().getSheetName())
        transformer.write()




    def _calculateTrip(self, device, positions, startIndex, endIndex, ignoreOdometer):
        startTrip = positions[startIndex]
        endTrip = positions[endIndex]

        speedMax = 0
        for i in range(startIndex, endIndex + 1):
            speed = positions[i].getSpeed()
            if speed > speedMax:
                speedMax = speed

        trip = TripReportItem()

        tripDuration = endTrip.getFixTime().getTime() - startTrip.getFixTime().getTime()
        deviceId = startTrip.getDeviceId()
        trip.setDeviceId(deviceId)
        trip.setDeviceName(device.getName())

        trip.setStartPositionId(startTrip.getId())
        trip.setStartLat(startTrip.getLatitude())
        trip.setStartLon(startTrip.getLongitude())
        trip.setStartTime(startTrip.getFixTime())
        startAddress = startTrip.getAddress()
        if startAddress is None and self._geocoder is not None and self._config.getBoolean(Keys.GEOCODER_ON_REQUEST):
            startAddress = self._geocoder.getAddress(startTrip.getLatitude(), startTrip.getLongitude(), None)
        trip.setStartAddress(startAddress)

        trip.setEndPositionId(endTrip.getId())
        trip.setEndLat(endTrip.getLatitude())
        trip.setEndLon(endTrip.getLongitude())
        trip.setEndTime(endTrip.getFixTime())
        endAddress = endTrip.getAddress()
        if endAddress is None and self._geocoder is not None and self._config.getBoolean(Keys.GEOCODER_ON_REQUEST):
            endAddress = self._geocoder.getAddress(endTrip.getLatitude(), endTrip.getLongitude(), None)
        trip.setEndAddress(endAddress)

        trip.setDistance(PositionUtil.calculateDistance(startTrip, endTrip, (not ignoreOdometer)))
        trip.setDuration(tripDuration)
        if tripDuration > 0:

            trip.setAverageSpeed(UnitsConverter.knotsFromMps(trip.getDistance() * 1000 / tripDuration))
        trip.setMaxSpeed(speedMax)
        trip.setSpentFuel(self.calculateFuel(startTrip, endTrip))

        trip.setDriverUniqueId(self.findDriver(startTrip, endTrip))
        trip.setDriverName(self.findDriverName(trip.getDriverUniqueId()))

        if (not ignoreOdometer) and startTrip.getDouble(Position.KEY_ODOMETER) != 0 and endTrip.getDouble(
                Position.KEY_ODOMETER) != 0:
            trip.setStartOdometer(startTrip.getDouble(Position.KEY_ODOMETER))
            trip.setEndOdometer(endTrip.getDouble(Position.KEY_ODOMETER))
        else:
            trip.setStartOdometer(startTrip.getDouble(Position.KEY_TOTAL_DISTANCE))
            trip.setEndOdometer(endTrip.getDouble(Position.KEY_TOTAL_DISTANCE))

        return trip


    def _calculateStop(self, device, positions, startIndex, endIndex, ignoreOdometer):
        startStop = positions[startIndex]
        endStop = positions[endIndex]

        stop = StopReportItem()

        deviceId = startStop.getDeviceId()
        stop.setDeviceId(deviceId)
        stop.setDeviceName(device.getName())

        stop.setPositionId(startStop.getId())
        stop.setLatitude(startStop.getLatitude())
        stop.setLongitude(startStop.getLongitude())
        stop.setStartTime(startStop.getFixTime())
        address = startStop.getAddress()
        if address is None and self._geocoder is not None and self._config.getBoolean(Keys.GEOCODER_ON_REQUEST):
            address = self._geocoder.getAddress(stop.getLatitude(), stop.getLongitude(), None)
        stop.setAddress(address)

        stop.setEndTime(endStop.getFixTime())

        stopDuration = endStop.getFixTime().getTime() - startStop.getFixTime().getTime()
        stop.setDuration(stopDuration)
        stop.setSpentFuel(self.calculateFuel(startStop, endStop))

        if startStop.hasAttribute(Position.KEY_HOURS) and endStop.hasAttribute(Position.KEY_HOURS):
            stop.setEngineHours(endStop.getLong(Position.KEY_HOURS) - startStop.getLong(Position.KEY_HOURS))

        if (not ignoreOdometer) and startStop.getDouble(Position.KEY_ODOMETER) != 0 and endStop.getDouble(
                Position.KEY_ODOMETER) != 0:
            stop.setStartOdometer(startStop.getDouble(Position.KEY_ODOMETER))
            stop.setEndOdometer(endStop.getDouble(Position.KEY_ODOMETER))
        else:
            stop.setStartOdometer(startStop.getDouble(Position.KEY_TOTAL_DISTANCE))
            stop.setEndOdometer(endStop.getDouble(Position.KEY_TOTAL_DISTANCE))

        return stop





    def _calculateTripOrStop(self, device, positions, startIndex, endIndex, ignoreOdometer, reportClass):
        if reportClass is TripReportItem.__class__:
            return self._calculateTrip(device, positions, startIndex, endIndex, ignoreOdometer)
        else:
            return self._calculateStop(device, positions, startIndex, endIndex, ignoreOdometer)


    def _isMoving(self, positions, index, tripsConfig):
        if tripsConfig.getMinimalNoDataDuration() > 0:
            beforeGap = index < len(positions) - 1 and positions[index + 1].getFixTime().getTime() - positions[
                index].getFixTime().getTime() >= tripsConfig.getMinimalNoDataDuration()
            afterGap = index > 0 and positions[index].getFixTime().getTime() - positions[
                index - 1].getFixTime().getTime() >= tripsConfig.getMinimalNoDataDuration()
            if beforeGap or afterGap:
                return False
        return positions[index].getBoolean(Position.KEY_MOTION)






    def detectTripsAndStops(self, device, positionCollection, ignoreOdometer, reportClass):
        result = []
        tripsConfig = TripsConfig(AttributeUtil.StorageProvider(self._config, self._storage, self._permissionsService, device))

        positions = list(positionCollection)
        if positions:
            trips = reportClass is TripReportItem.__class__

            motionState = MotionState()
            initialValue = self._isMoving(positions, 0, tripsConfig)
            motionState.setMotionStreak(initialValue)
            motionState.setMotionState(initialValue)

            detected = trips == motionState.getMotionState()
            startEventIndex = 0 if detected else -1
            startNoEventIndex = -1
            for i, unusedItem in enumerate(positions):
                motion = self._isMoving(positions, i, tripsConfig)
                if motionState.getMotionState() != motion:
                    if motion == trips:
                        startEventIndex = startEventIndex if detected else i
                        startNoEventIndex = -1
                    else:
                        startNoEventIndex = i

                MotionProcessor.updateState(motionState, positions[i], motion, tripsConfig)
                if motionState.getEvent() is not None:
                    if motion == trips:
                        detected = True
                        startNoEventIndex = -1
                    elif startEventIndex >= 0 and startNoEventIndex >= 0:
                        result.add(
                            self._calculateTripOrStop(device, positions, startEventIndex, startNoEventIndex, ignoreOdometer,
                                                reportClass))
                        detected = False
                        startEventIndex = -1
                        startNoEventIndex = -1
            if detected & startEventIndex >= 0 and startEventIndex < len(positions) - 1:
                endIndex = startNoEventIndex if startNoEventIndex >= 0 else len(positions) - 1
                result.add(self._calculateTripOrStop(device, positions, startEventIndex, endIndex, ignoreOdometer, reportClass))

        return result
