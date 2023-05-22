from .geofenceGeometry import GeofenceGeometry

class GeofencePolygon(GeofenceGeometry):

    def _initialize_instance_fields(self):

        self._coordinates = None
        self._constant = None
        self._multiple = None
        self._needNormalize = False




    def __init__(self):
        self._initialize_instance_fields()





    def __init__(self, wkt):
        self._initialize_instance_fields()

        self.fromWkt(wkt)




    def _preCalculate(self):
        if self._coordinates is None:
            return

        polyCorners = len(self._coordinates)
        i = 0
        j = polyCorners - 1

        if self._constant is not None:
            self._constant = None
        if self._multiple is not None:
            self._multiple = None

        self._constant = [0 for _ in range(polyCorners)]
        self._multiple = [0 for _ in range(polyCorners)]

        hasNegative = False
        hasPositive = False
        for i in range(0, polyCorners):
            if self._coordinates[i].getLon() > 90:
                hasPositive = True
            elif self._coordinates[i].getLon() < -90:
                hasNegative = True
        self._needNormalize = hasPositive and hasNegative

        i = 0

        while i < polyCorners:
            if self._normalizeLon(self._coordinates[j].getLon()) == self._normalizeLon(self._coordinates[i].getLon()):
                self._constant[i] = self._coordinates[i].getLat()
                self._multiple[i] = 0
            else:
                self._constant[i] = self._coordinates[i].getLat() - (self._normalizeLon(self._coordinates[i].getLon()) * self._coordinates[j].getLat()) / (self._normalizeLon(self._coordinates[j].getLon()) - self._normalizeLon(self._coordinates[i].getLon())) + (self._normalizeLon(self._coordinates[i].getLon()) * self._coordinates[i].getLat()) / (self._normalizeLon(self._coordinates[j].getLon()) - self._normalizeLon(self._coordinates[i].getLon()))
                self._multiple[i] = (self._coordinates[j].getLat() - self._coordinates[i].getLat()) / (self._normalizeLon(self._coordinates[j].getLon()) - self._normalizeLon(self._coordinates[i].getLon()))
            j = i

    def _normalizeLon(self, lon):
        if self._needNormalize and lon < -90:
            return lon + 360
        return lon

    def containsPoint(self, config, geofence, latitude, longitude):

        polyCorners = len(self._coordinates)
        i = 0
        j = polyCorners - 1
        longitudeNorm = self._normalizeLon(longitude)
        oddNodes = False

        i = 0

        while i < polyCorners:
            if self._normalizeLon(self._coordinates[i].getLon()) < longitudeNorm and self._normalizeLon(self._coordinates[j].getLon()) >= longitudeNorm or self._normalizeLon(self._coordinates[j].getLon()) < longitudeNorm and self._normalizeLon(self._coordinates[i].getLon()) >= longitudeNorm:
                oddNodes ^= longitudeNorm * self._multiple[i] + self._constant[i] < latitude
            j = i
        return oddNodes

    def calculateArea(self):
        jtsShapeFactory = "(JtsSpatialContextFactory()).newSpatialContext().getShapeFactory()"
        polygonBuilder = jtsShapeFactory.polygon()
        for coordinate in self._coordinates:
            polygonBuilder.pointXY(coordinate.getLon(), coordinate.getLat())
        return "polygonBuilder.build().getArea(SpatialContext.GEO) * DEG_TO_KM * DEG_TO_KM"

    def calculateArea(self):
        jtsShapeFactory = "(JtsSpatialContextFactory()).newSpatialContext().getShapeFactory()"
        polygonBuilder = jtsShapeFactory.polygon()
        for coordinate in self._coordinates:
            polygonBuilder.pointXY(coordinate.getLon(), coordinate.getLat())
        return "polygonBuilder.build().getArea(SpatialContext.GEO) * DEG_TO_KM * DEG_TO_KM"

    def toWkt(self):
        buf = ""
        buf += ("POLYGON ((")
        for coordinate in self._coordinates:
            buf += (coordinate.getLat())
            buf += (" ")
            buf += (coordinate.getLon())
            buf += (", ")
        return buf.substring(0, buf.length() - 2) + "))"


    def fromWkt(self, wkt):
        if self._coordinates is None:
            self._coordinates = []
        else:
            self._coordinates.clear()

        if not wkt.startswith("POLYGON"):
            raise Exception("Mismatch geometry type", 0)
        content = wkt[wkt.find("((") + 2:wkt.find("))")]
        if not content:
            raise Exception("No content", 0)
        commaTokens = content.split(",")
        if len(commaTokens) < 3:
            raise Exception("Not valid content", 0)

        for commaToken in commaTokens:
            tokens = commaToken.trim().split("\\s")
            if len(tokens) != 2:
                raise Exception("Here must be two coordinates: " + commaToken, 0)
            coordinate = self.Coordinate()
            try:
                coordinate.setLat(float(tokens[0]))
            except Exception as e:
                raise Exception(tokens[0] + " is not a double", 0)
            try:
                coordinate.setLon(float(tokens[1]))
            except Exception as e:
                raise Exception(tokens[1] + " is not a double", 0)
            self._coordinates.add(coordinate)

        self._preCalculate()
