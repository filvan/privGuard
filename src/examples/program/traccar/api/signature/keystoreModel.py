from src.examples.program.traccar.model.baseModel import BaseModel
from src.examples.program.traccar.storage.storageName import StorageName

class KeystoreModel(BaseModel):

    def __init__(self):
        #instance fields found by Java to Python Converter:
        self._publicKey = None
        self._privateKey = None



    def getPublicKey(self):
        return self._publicKey

    def setPublicKey(self, publicKey):
        self._publicKey = publicKey


    def getPrivateKey(self):
        return self._privateKey

    def setPrivateKey(self, privateKey):
        self._privateKey = privateKey
