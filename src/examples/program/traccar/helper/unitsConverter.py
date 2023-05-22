class UnitsConverter:

    _KNOTS_TO_KPH_RATIO = 0.539957
    _KNOTS_TO_MPH_RATIO = 0.868976
    _KNOTS_TO_MPS_RATIO = 1.94384
    _KNOTS_TO_CPS_RATIO = 0.0194384449
    _METERS_TO_FEET_RATIO = 0.3048
    _METERS_TO_MILE_RATIO = 1609.34
    _MILLISECONDS_TO_HOURS_RATIO = 3600000
    _MILLISECONDS_TO_MINUTES_RATIO = 60000

    def __init__(self):
        pass

    @staticmethod
    def knotsFromKph(value):
        return value * UnitsConverter._KNOTS_TO_KPH_RATIO

    @staticmethod
    def kphFromKnots(value):
        return value / UnitsConverter._KNOTS_TO_KPH_RATIO

    @staticmethod
    def knotsFromMph(value):
        return value * UnitsConverter._KNOTS_TO_MPH_RATIO

    @staticmethod
    def mphFromKnots(value):
        return value / UnitsConverter._KNOTS_TO_MPH_RATIO

    @staticmethod
    def knotsFromMps(value):
        return value * UnitsConverter._KNOTS_TO_MPS_RATIO

    @staticmethod
    def mpsFromKnots(value):
        return value / UnitsConverter._KNOTS_TO_MPS_RATIO

    @staticmethod
    def knotsFromCps(value):
        return value * UnitsConverter._KNOTS_TO_CPS_RATIO

    @staticmethod
    def feetFromMeters(value):
        return value / UnitsConverter._METERS_TO_FEET_RATIO

    @staticmethod
    def metersFromFeet(value):
        return value * UnitsConverter._METERS_TO_FEET_RATIO

    @staticmethod
    def milesFromMeters(value):
        return value / UnitsConverter._METERS_TO_MILE_RATIO

    @staticmethod
    def metersFromMiles(value):
        return value * UnitsConverter._METERS_TO_MILE_RATIO

    @staticmethod

    def msFromHours(value):
        return value * UnitsConverter._MILLISECONDS_TO_HOURS_RATIO

    @staticmethod

    def msFromHours(value):
        return int((value * UnitsConverter._MILLISECONDS_TO_HOURS_RATIO))

    @staticmethod
    def msFromMinutes(value):
        return value * UnitsConverter._MILLISECONDS_TO_MINUTES_RATIO
