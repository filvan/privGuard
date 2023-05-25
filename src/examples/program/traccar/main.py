import collections
import locale
import sys
from email.charset import Charset
from msilib.schema import File
from threading import Thread

from matplotlib.backends.backend_pdf import Stream

from src.examples.program.traccar.broadcast.broadcastService import BroadcastService
from src.examples.program.traccar.helper.model.deviceUtil import DeviceUtil
from src.examples.program.traccar.schedule.scheduleManager import ScheduleManager
from src.examples.program.traccar.serverManager import ServerManager
from src.examples.program.traccar.storage.databaseModule import DatabaseModule
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.web.webModule import WebModule
from src.examples.program.traccar.web.webServer import WebServer
from src.examples.program.traccar.windowsService import WindowsService


class Main:

    _LOGGER = "LoggerFactory.getLogger(Main.__class__)"

    _injector = None

    @staticmethod
    def getInjector():
        return Main._injector

    def __init__(self):
        pass

    @staticmethod
    def logSystemInfo():
        try:
            operatingSystemBean = "ManagementFactory.getOperatingSystemMXBean()"
            Main._LOGGER.info("Operating system" + " name: " + operatingSystemBean.getName() + " version: " + operatingSystemBean.getVersion() + " architecture: " + operatingSystemBean.getArch())

            runtimeBean = "ManagementFactory.getRuntimeMXBean()"
            Main._LOGGER.info("Java runtime" + " name: " + runtimeBean.getVmName() + " vendor: " + runtimeBean.getVmVendor() + " version: " + runtimeBean.getVmVersion())

            memoryBean = "ManagementFactory.getMemoryMXBean()"
            Main._LOGGER.info("Memory limit" + " heap: " + memoryBean.getHeapMemoryUsage().getMax() / (1024 * 1024) + "mb" + " non-heap: " + memoryBean.getNonHeapMemoryUsage().getMax() / (1024 * 1024) + "mb")

            Main._LOGGER.info("Character encoding: " + sys.getProperty("file.encoding") + " charset: " + Charset.defaultCharset())

        except Exception as error:
            Main._LOGGER.warn("Failed to get system info")

    @staticmethod
    def main(args):
        locale.setDefault(locale.ENGLISH)
        configFile = None
        if len(args) <= 0:
            configFile = "./debug.xml"
            if not(File(configFile)).exists():
                raise Exception("Configuration file is not provided")
        else:
            configFile = args[len(args) - 1]

        if len(args) > 0 and args[0].startswith("--"):
            windowsService = Main.WindowsServiceAnonymousInnerClass(configFile)
            if args[0] == "--install":
                windowsService.install("traccar", None, None, None, None, configFile)
                return
            elif args[0] == "--uninstall":
                windowsService.uninstall()
                return
            else:
                windowsService.init()
        else:
            Main.run(configFile)

    class WindowsServiceAnonymousInnerClass(WindowsService):

        def __init__(self, configFile):
            super().__init__("traccar")
            self._configFile = configFile

        def run(self):
            Main.run(self._configFile)

    @staticmethod
    def run(configFile):
        try:
            Main._injector = "Guice.createInjector(MainModule(configFile), DatabaseModule(), WebModule())"
            Main.logSystemInfo()
            Main._LOGGER.info("Version: " + Main.__class__.getPackage().getImplementationVersion())
            Main._LOGGER.info("Starting server...")

            if Main._injector.getInstance(BroadcastService.__class__).singleInstance():
                DeviceUtil.resetStatus(Main._injector.getInstance(Storage.__class__))

            services = Stream.of(ServerManager.__class__, WebServer.__class__, ScheduleManager.__class__, BroadcastService.__class__).map(Main._injector.getInstance()).filter(object.nonNull()).collect(collections.toList())

            for service in services:
                service.start()

            Thread.setDefaultUncaughtExceptionHandler(lambda t, e : Main._LOGGER.error("Thread exception", e))

            #JAVA TO PYTHON CONVERTER TASK: Only expression lambdas are converted by Java to Python Converter:
            #            Runtime.getRuntime().addShutdownHook(new Thread(() ->
            #            {
            #                LOGGER.info("Stopping server...")
            #
            #                for (var service : services)
            #                {
            #                    try
            #                    {
            #                        service.stop()
            #                    }
            #                    catch (Exception e)
            #                    {
            #                        throw new RuntimeException(e)
            #                    }
            #                }
            #            }
            #            ))
        except Exception as e:
            Main._LOGGER.error("Main method error", e)
            raise Exception(e)


def main():
    Main.main([])

if __name__ == "__main__":
    main()
