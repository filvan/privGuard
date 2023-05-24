from src.examples.program.traccar.helper.dateUtil import DateUtil
from src.examples.program.traccar.helper.model.positionUtil import PositionUtil
from src.examples.program.traccar.model.device import Device
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.condition import Condition
from src.examples.program.traccar.storage.query.request import Request

class GpxExportProvider:

    def __init__(self, storage):
        self._storage = None

        self._storage = storage


    def generate(self, outputStream, deviceId, from_, to):

        device = self._storage.getObject(Device.__class__, Request(Columns.All(), Condition.Equals("id", deviceId)))
        positions = PositionUtil.getPositions(self._storage, deviceId, from_, to)

        with "PrintWriter(outputStream)" as writer:
            writer.print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
            writer.print("<gpx version=\"1.0\">")
            writer.print("<trk>")
            writer.print("<name>")
            writer.print(device.getName())
            writer.print("</name>")
            writer.print("<trkseg>")
            #            positions.forEach(position ->
            #            {
            #                writer.print("<trkpt lat=\"")
            #                writer.print(position.getLatitude())
            #                writer.print("\" lon=\"")
            #                writer.print(position.getLongitude())
            #                writer.print("\">")
            #                writer.print("<ele>")
            #                writer.print(position.getAltitude())
            #                writer.print("</ele>")
            #                writer.print("<time>")
            #                writer.print(DateUtil.formatDate(position.getFixTime()))
            #                writer.print("</time>")
            #                writer.print("</trkpt>")
            #            }
            #            )
            writer.print("</trkseg>")
            writer.print("</trk>")
            writer.print("</gpx>")
