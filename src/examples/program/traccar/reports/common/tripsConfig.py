from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.helper.model.attributeUtil import AttributeUtil

class TripsConfig:

    def _initialize_instance_fields(self):

        self._minimalTripDistance = 0
        self._minimalTripDuration = 0
        self._minimalParkingDuration = 0
        self._minimalNoDataDuration = 0
        self._useIgnition = False


    def __init__(self, attributeProvider):
        self(AttributeUtil.lookup(attributeProvider, Keys.REPORT_TRIP_MINIMAL_TRIP_DISTANCE), AttributeUtil.lookup(attributeProvider, Keys.REPORT_TRIP_MINIMAL_TRIP_DURATION) * 1000, AttributeUtil.lookup(attributeProvider, Keys.REPORT_TRIP_MINIMAL_PARKING_DURATION) * 1000, AttributeUtil.lookup(attributeProvider, Keys.REPORT_TRIP_MINIMAL_NO_DATA_DURATION) * 1000, AttributeUtil.lookup(attributeProvider, Keys.REPORT_TRIP_USE_IGNITION))

    def __init__(self, minimalTripDistance, minimalTripDuration, minimalParkingDuration, minimalNoDataDuration, useIgnition):
        self._initialize_instance_fields()

        self._minimalTripDistance = minimalTripDistance
        self._minimalTripDuration = minimalTripDuration
        self._minimalParkingDuration = minimalParkingDuration
        self._minimalNoDataDuration = minimalNoDataDuration
        self._useIgnition = useIgnition


    def getMinimalTripDistance(self):
        return self._minimalTripDistance


    def getMinimalTripDuration(self):
        return self._minimalTripDuration


    def getMinimalParkingDuration(self):
        return self._minimalParkingDuration


    def getMinimalNoDataDuration(self):
        return self._minimalNoDataDuration


    def getUseIgnition(self):
        return self._useIgnition
