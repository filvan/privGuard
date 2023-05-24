import collections

from src.examples.program.traccar.helper.model.positionUtil import PositionUtil
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class KmlExportProvider:
    def __init__(self, storage):
        self._storage = None

        self._storage = storage

    def generate(self, outputStream, deviceId, from_, to):

        device = self._storage.getObject(Device.__class__, Request(Columns.All(), Condition.Equals("id", deviceId)))
        positions = PositionUtil.getPositions(self._storage, deviceId, from_, to)

        dateFormat = format("yyyy-MM-dd HH:mm")

        with "PrintWriter(outputStream)" as writer:
            writer.print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
            writer.print("<kml xmlns=\"http://www.opengis.net/kml/2.2\">")
            writer.print("<Document>")
            writer.print("<name>")
            writer.print(device.getName())
            writer.print("</name>")
            writer.print("<Placemark>")
            writer.print("<name>")
            writer.print(dateFormat.format(from_))
            writer.print(" - ")
            writer.print(dateFormat.format(to))
            writer.print("</name>")
            writer.print("<LineString>")
            writer.print("<extrude>1</extrude>")
            writer.print("<tessellate>1</tessellate>")
            writer.print("<altitudeMode>absolute</altitudeMode>")
            writer.print("<coordinates>")
            writer.print(positions.stream().map((lambda p : "{0:f},{1:f},{2:f}".format(p.getLongitude(), p.getLatitude(), p.getAltitude()))).collect(collections.joining(" ")))
            writer.print("</coordinates>")
            writer.print("</LineString>")
            writer.print("</Placemark>")
            writer.print("</Document>")
            writer.print("</kml>")
