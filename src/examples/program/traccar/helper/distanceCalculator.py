import math

class DistanceCalculator:

    def __init__(self):
        pass

    _EQUATORIAL_EARTH_RADIUS = 6378.1370
    _DEG_TO_RAD = math.pi / 180

    @staticmethod
    def distance(lat1, lon1, lat2, lon2):
        dlong = (lon2 - lon1) * DistanceCalculator._DEG_TO_RAD
        dlat = (lat2 - lat1) * DistanceCalculator._DEG_TO_RAD
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1 * DistanceCalculator._DEG_TO_RAD) * math.cos(lat2 * DistanceCalculator._DEG_TO_RAD) * math.sin(dlong / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = DistanceCalculator._EQUATORIAL_EARTH_RADIUS * c
        return d * 1000

    @staticmethod
    def distanceToLine(pointLat, pointLon, lat1, lon1, lat2, lon2):
        d0 = DistanceCalculator.distance(pointLat, pointLon, lat1, lon1)
        d1 = DistanceCalculator.distance(lat1, lon1, lat2, lon2)
        d2 = DistanceCalculator.distance(lat2, lon2, pointLat, pointLon)
        if d0 ** 2 > d1 ** 2 + d2 ** 2:
            return d2
        if d2 ** 2 > d1 ** 2 + d0 ** 2:
            return d0
        halfP = (d0 + d1 + d2) * 0.5
        area = math.sqrt(halfP * (halfP - d0) * (halfP - d1) * (halfP - d2))
        return 2 * area / d1
