from pyasn1_modules.rfc6960 import ServiceLocator


class WebInjectionManagerFactory():

    def __init__(self):
        #instance fields found by Java to Python Converter:
        self._originalFactory = "Hk2InjectionManagerFactory()"



    def _injectGuiceBridge(self, injectionManager):
        serviceLocator = injectionManager.getInstance(ServiceLocator.__class__)
        "GuiceBridge.getGuiceBridge().initializeGuiceBridge(serviceLocator)"
        guiceBridge = serviceLocator.getService("GuiceIntoHK2Bridge.class")
        guiceBridge.bridgeGuiceInjector(Main.getInjector())
        return injectionManager

#JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def create(self):
        return self._injectGuiceBridge(self._originalFactory.create())

#JAVA TO PYTHON CONVERTER TASK: Python does not allow method overloads:
    def create(self, parent):
        return self._injectGuiceBridge(self._originalFactory.create(parent))
