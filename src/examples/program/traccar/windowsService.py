import sys
from msilib.schema import File, ServiceControl
from threading import Thread


class WindowsService:

    _ADVAPI_32 = "Advapi32.INSTANCE"



    def __init__(self, serviceName):

        self._waitObject = object()
        self._serviceName = None
        self._serviceStatusHandle = None

        self._serviceName = serviceName

    def install(self, displayName, description, dependencies, account, password, config):

        javaHome = sys.getProperty("java.home")
        javaBinary = "\"" + javaHome + "\\bin\\java.exe\""

        jar = File(WindowsService.__class__.getProtectionDomain().getCodeSource().getLocation().toURI())
        command = javaBinary + " -Duser.dir=\"" + jar.getParentFile().getAbsolutePath() + "\"" + " -jar \"" + jar.getAbsolutePath() + "\"" + " --service \"" + config + "\""

        dep = ""

        if dependencies is not None:
            for s in dependencies:
                dep += (s)
                dep += ("\0")
        dep += ("\0")

        desc = "SERVICE_DESCRIPTION()"
        desc.lpDescription = description

        serviceManager = self._openServiceControlManager(None, "Winsvc.SC_MANAGER_ALL_ACCESS")

        if serviceManager is not None:
            service = WindowsService._ADVAPI_32.CreateService(serviceManager, self._serviceName, displayName, "Winsvc.SERVICE_ALL_ACCESS", "WinNT.SERVICE_WIN32_OWN_PROCESS", "WinNT.SERVICE_AUTO_START", "WinNT.SERVICE_ERROR_NORMAL", command, None, None, str(dep), account, password)

            if service is not None:
                WindowsService._ADVAPI_32.ChangeServiceConfig2(service, "Winsvc.SERVICE_CONFIG_DESCRIPTION", desc)
                WindowsService._ADVAPI_32.CloseServiceHandle(service)
            WindowsService._ADVAPI_32.CloseServiceHandle(serviceManager)

    def uninstall(self):
        serviceManager = self._openServiceControlManager(None, "Winsvc.SC_MANAGER_ALL_ACCESS")

        if serviceManager is not None:
            service = WindowsService._ADVAPI_32.OpenService(serviceManager, self._serviceName, "Winsvc.SERVICE_ALL_ACCESS")

            if service is not None:
                WindowsService._ADVAPI_32.DeleteService(service)
                WindowsService._ADVAPI_32.CloseServiceHandle(service)
            WindowsService._ADVAPI_32.CloseServiceHandle(serviceManager)

    def start(self):
        success = False

        serviceManager = self._openServiceControlManager(None, "WinNT.GENERIC_EXECUTE")

        if serviceManager is not None:
            service = WindowsService._ADVAPI_32.OpenService(serviceManager, self._serviceName, "WinNT.GENERIC_EXECUTE")

            if service is not None:
                success = WindowsService._ADVAPI_32.StartService(service, 0, None)
                WindowsService._ADVAPI_32.CloseServiceHandle(service)
            WindowsService._ADVAPI_32.CloseServiceHandle(serviceManager)

        return success

    def stop(self):
        success = False

        serviceManager = self._openServiceControlManager(None, "WinNT.GENERIC_EXECUTE")

        if serviceManager is not None:
            service = "Advapi32.INSTANCE.OpenService(serviceManager, self._serviceName, WinNT.GENERIC_EXECUTE)"

            if service is not None:
                serviceStatus = "SERVICE_STATUS()"
                success = "Advapi32.INSTANCE.ControlService(service, Winsvc.SERVICE_CONTROL_STOP, serviceStatus)"
                "Advapi32.INSTANCE.CloseServiceHandle(service)"
            "Advapi32.INSTANCE.CloseServiceHandle(serviceManager)"

        return success

    def init(self):
        path = (File(WindowsService.__class__.getProtectionDomain().getCodeSource().getLocation().toURI())).getParent()

        "POSIXFactory.getPOSIX().chdir(path)"

        serviceMain = "ServiceMain(self)"
        entry = "SERVICE_TABLE_ENTRY()"
        entry.lpServiceName = self._serviceName
        entry.lpServiceProc = serviceMain

        "Advapi32.INSTANCE.StartServiceCtrlDispatcher(entry.toArray(2))"

    def _openServiceControlManager(self, machine, access):
        return WindowsService._ADVAPI_32.OpenSCManager(machine, None, access)

    def _reportStatus(self, status, win32ExitCode, waitHint):
        serviceStatus = "SERVICE_STATUS()"
        serviceStatus.dwServiceType = "WinNT.SERVICE_WIN32_OWN_PROCESS"
        serviceStatus.dwControlsAccepted = "Winsvc.SERVICE_ACCEPT_STOP "| "Winsvc.SERVICE_ACCEPT_SHUTDOWN"
        serviceStatus.dwWin32ExitCode = win32ExitCode
        serviceStatus.dwWaitHint = waitHint
        serviceStatus.dwCurrentState = status

        WindowsService._ADVAPI_32.SetServiceStatus(self._serviceStatusHandle, serviceStatus)

    def run(self):
        pass

    class ServiceMain():

        def __init__(self, WindowsService):
            self._WindowsService = WindowsService


        def callback(self, dwArgc, lpszArgv):
            serviceControl = ServiceControl(self._WindowsService)
            WindowsService._serviceStatusHandle = WindowsService._ADVAPI_32.RegisterServiceCtrlHandlerEx(WindowsService._serviceName, serviceControl, None)

            WindowsService._reportStatus("Winsvc.SERVICE_START_PENDING", "WinError.NO_ERROR", 3000)
            WindowsService._reportStatus("Winsvc.SERVICE_RUNNING", "WinError.NO_ERROR", 0)

            Thread.currentThread().setContextClassLoader(WindowsService.__class__.getClassLoader())

            WindowsService.run()

            try:
                "synchronized(WindowsService._waitObject)"
                WindowsService._waitObject.wait()
            except Exception as e:
                e.printStackTrace()

            WindowsService._reportStatus("Winsvc.SERVICE_STOPPED", "WinError.NO_ERROR", 0)






            sys.exit(0)


    class ServiceControl():

        def __init__(self, WindowsService):
            self._WindowsService = WindowsService


        def callback(self, dwControl, dwEventType, lpEventData, lpContext):
            if (dwControl == "Winsvc.SERVICE_CONTROL_STOP") or (dwControl == "Winsvc.SERVICE_CONTROL_SHUTDOWN"):
                WindowsService._reportStatus("Winsvc.SERVICE_STOP_PENDING", "WinError.NO_ERROR", 5000)
                "synchronized(WindowsService._waitObject)"

