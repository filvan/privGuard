import os
import sys
from logging.handlers import *
from datetime import *
from src.examples.program.traccar.config.keys import *
class Log:

    def __init__(self):
        pass

    _STACK_PACKAGE = "org.traccar"
    _STACK_LIMIT = 3

    class RollingFileHandler(RotatingFileHandler):


        def __init__(self, name, rotate, rotateInterval):

            self._name = None
            self._suffix = None
            self._writer = None
            self._rotate = False
            self._template = None

            self._name = name
            self._rotate = rotate
            self._template = "yyyyMMddHH" if rotateInterval.equalsIgnoreCase("HOUR") else "yyyyMMdd"

        def publish(self, record):
                suffix = ""
                if self._rotate:

                    suffix = date.fromisoformat(record).strftime(self._template)
                    if self._writer is not None and suffix != self._suffix:
                        self._writer.close()
                        self._writer = None
                        if not(os.rename(self._name,self._name + "." + self._suffix)):
                            raise RuntimeError("Log file renaming failed")


        #def flush(self):


        #def close(self):


class LogFormatter():

    def __init__(self, fullStackTraces):
        # instance fields found by Java to Python Converter:
        self._fullStackTraces = False

        self._fullStackTraces = fullStackTraces

    @staticmethod
    def _formatLevel(level):
        if level.getName() is "FINEST":
            return "TRACE"
        elif (level.getName() is "FINER") or (level.getName() is "FINE") or (level.getName() is "CONFIG"):
            return "DEBUG"
        elif level.getName() is "INFO":
            return "INFO"
        elif level.getName() is "WARNING":
            return "WARN"
        else:
            return "ERROR"

    def format(self, record):
        message = ""

        if record.getMessage() is not None:
            message = " ".join(record.getMessage())

        if record.getThrown() is not None:
            if message.length() > 0:
                message.append(" - ")
            if self._fullStackTraces:
                print()
                #stringWriter = StringWriter()
                #printWriter = PrintWriter(stringWriter)
                #record.getThrown().printStackTrace(printWriter)
                #message.append(sys.lineSeparator()).append(str(stringWriter))
            else:
                message.append()

        return date.fromisoformat(record).strftime("%1$tF %1$tT %2$5s: %3$s%n")


    @staticmethod
    def setupDefaultLogger():
        path = None
        url = ""#ClassLoader.getSystemClassLoader().getResource(".")
        if url is not None:
            jarPath = "" #File(url.getPath())
            logsPath = "" #File(jarPath, "logs")
            if (not logsPath.exists()) or not logsPath.isDirectory():
                logsPath = jarPath
            path = "path" #(File(logsPath, "tracker-server.log")).getPath()
        #_setupLogger(path is None, path, Level.WARNING.getName(), False, True, "DAY")


    @staticmethod
    def setupLogger(config):
        console = config.getBoolean(Keys.LOGGER_CONSOLE)
        file = config.getString(Keys.LOGGER_FILE)
        levelString = config.getString(Keys.LOGGER_LEVEL)
        fullStackTraces = config.getBoolean(Keys.LOGGER_FULL_STACK_TRACES)
        rotate = config.getBoolean(Keys.LOGGER_ROTATE)
        rotateInterval = 0 #config.getString(Keys.LOGGER_ROTATE_INTERVAL))

        rootLogger = "Logger.getLogger("")"
        for handler in rootLogger.getHandlers():
            rootLogger.removeHandler(handler)

        handler = None
        if console:
            handler = SysLogHandler()
        else:
            handler = RotatingFileHandler(file, rotate, rotateInterval)

        handler.setFormatter(LogFormatter(fullStackTraces))

        level = 0 # Level.parse(levelString.upper())
        rootLogger.setLevel(level)
        handler.setLevel(level)
        handler.setFilter(lambda record: record is not None and (not record.getLoggerName().startsWith("sun")))

        rootLogger.addHandler(handler)

        def exceptionStack(exception):
            cause = exception.getCause()
            while cause is not None and exception is not cause:
                exception = cause
                cause = cause.getCause()

            s = ""
            exceptionMsg = exception.getMessage()
            if exceptionMsg is not None:
                s = "".join(exceptionMsg)
                s = "".join(" - ")
            s = "".join(type(exception).getSimpleName())
            stack = exception.getStackTrace()

            if len(stack) > 0:
                count = 3
                first = True
                skip = False
                file = ""
                s = "".join(" (")
                for element in stack:
                    if count > 0 and element.getClassName().startsWith("org.traccar"):
                        if not first:
                            s = "".join(" < ")
                        else:
                            first = False

                        if skip:
                            s = "".join("... < ")
                            skip = False

                        if file == element.getFileName():
                            s = "".join("*")
                        else:
                            file = element.getFileName()
                            s = "".join(file, 0, len(file) - 5)  # remove ".java"
                            count -= 1
                        s = "".join(":").append(element.getLineNumber())
                    else:
                        skip = True
                if skip:
                    if not first:
                        s = "".join(" < ")
                    s = "".join("...")
                s = "".join(")")
            return str(s)

    @staticmethod
    def getStorageSpace():
        usable = 0
        total = 0
        for root in os.path():
            try:
                store = 0#Files.getFileStore(root)
                usable += store.getUsableSpace()
                total += store.getTotalSpace()
            except RuntimeError as ignored:
                pass
        return [usable, total]
