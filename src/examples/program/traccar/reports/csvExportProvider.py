import collections

from src.examples.program.traccar.helper.dateUtil import DateUtil
from src.examples.program.traccar.helper.model.positionUtil import PositionUtil
from src.examples.program.traccar.model.position import Position
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.storage import Storage

class CsvExportProvider:


    def __init__(self, storage):

        self._storage = None

        self._storage = storage

    def generate(self, outputStream, deviceId, from_, to):

        positions = PositionUtil.getPositions(self._storage, deviceId, from_, to)

        attributes = positions.stream().flatMap((lambda position : position.getAttributes().keySet().stream())).collect(collections.toUnmodifiableSet())

        properties = list()
        properties.append("id", Position.getId())
        properties.append("deviceId", Position.getDeviceId())
        properties.append("protocol", Position.getProtocol())
        properties.append("serverTime", lambda position : DateUtil.formatDate(position.getServerTime()))
        properties.append("deviceTime", lambda position : DateUtil.formatDate(position.getDeviceTime()))
        properties.append("fixTime", lambda position : DateUtil.formatDate(position.getFixTime()))
        properties.append("valid", Position.getValid())
        properties.append("latitude", Position.getLatitude())
        properties.append("longitude", Position.getLongitude())
        properties.append("altitude", Position.getAltitude())
        properties.append("speed", Position.getSpeed())
        properties.append("course", Position.getCourse())
        properties.append("address", Position.getAddress())
        properties.append("accuracy", Position.getAccuracy())
        attributes.forEach(lambda key : properties.append(key, lambda position : position.getAttributes().get(key)))

        with "PrintWriter(outputStream)" as writer:
            writer.println(str.join(",", properties.keySet()))
            positions.forEach(lambda position : writer.println(properties.values().stream().map(lambda f : object.toString(f.apply(position), "")).collect(collections.joining(","))))
