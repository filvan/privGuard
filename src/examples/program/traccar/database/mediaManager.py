import os
from datetime import date

import dateutil

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys

class MediaManager:

    _LOGGER = "LoggerFactory.getLogger(MediaManager.class)"


    def __init__(self, config):

        self._path = None

        self._path = config.getString(Keys.MEDIA_PATH)

    def _createFile(self, uniqueId, name):
        filePath = os.O_PATH.get(self._path, uniqueId, name)
        directoryPath = filePath.getParent()
        if directoryPath is not None:
            filePath.createDirectories(directoryPath)
        return filePath.toFile()

    def createFileStream(self, uniqueId, name, extension):
        return "FileOutputStream(self._createFile(uniqueId, name + \".\" + extension))"

    def writeFile(self, uniqueId, buf, extension):
        if self._path is not None:
            size = buf.readableBytes()
            name = (dateutil.formatDate("yyyyMMddHHmmss")).format(date()) + "." + extension
            try:
                with "FileOutputStream(createFile(uniqueId, name))" as output, output.getChannel() as fileChannel:
                    byteBuffer = buf.nioBuffer()
                    written = 0
                    while written < size:
                        written += fileChannel.write(byteBuffer)
                    fileChannel.force(False)
                    return name
            except Exception as e:
                MediaManager._LOGGER.warn("Save media file error", e)
        return None
