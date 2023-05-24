import sys
from inspect import Signature

from src.examples.program.traccar.api.signature.keystoreModel import KeystoreModel
from src.examples.program.traccar.storage.storage import StorageException
from src.examples.program.traccar.storage.storageException import StorageException
from src.examples.program.traccar.storage.query.columns import Columns
from src.examples.program.traccar.storage.query.request import Request

class CryptoManager:





    def __init__(self, storage):

        self._storage = None
        self._publicKey = None
        self._privateKey = None

        self._storage = storage



    def sign(self, data):
        if self._privateKey is None:
            self._initializeKeys()
        signature = Signature.getInstance("SHA256withECDSA")
        signature.initSign(self._privateKey)
        signature.update(data)
        block = signature.sign()
        combined = [0 for _ in range(1 + len(block) + len(data))]
        combined[0] = int(len(block))
        sys.arraycopy(block, 0, combined, 1, len(block))
        sys.arraycopy(data, 0, combined, 1 + len(block), len(data))
        return combined



    def verify(self, data):
        if self._publicKey is None:
            self._initializeKeys()
        signature = Signature.getInstance("SHA256withECDSA")
        signature.initVerify(self._publicKey)
        length = data[0]
        originalData = [0 for _ in range(len(data) - 1 - length)]
        sys.arraycopy(data, 1 + length, originalData, 0, len(originalData))
        signature.update(originalData)
        if not signature.verify(data, 1, length):
            raise Exception("Invalid signature")
        return originalData



    def _initializeKeys(self):
        model = self._storage.getObject(KeystoreModel.__class__, Request(Columns.All()))
        if model is not None:
            self._publicKey =" KeyFactory.getInstance(\"EC\").generatePublic(X509EncodedKeySpec(model.getPublicKey()))"
            self._privateKey = "KeyFactory.getInstance(\"EC\").generatePrivate(PKCS8EncodedKeySpec(model.getPrivateKey()))"
        else:
            generator = "KeyPairGenerator".getInstance("EC")
            "generator.initialize(ECGenParameterSpec(\"secp256r1\"), SecureRandom())"
            pair = generator.generateKeyPair()

            self._publicKey = pair.getPublic()
            self._privateKey = pair.getPrivate()

            model = KeystoreModel()
            model.setPublicKey(self._publicKey.getEncoded())
            model.setPrivateKey(self._privateKey.getEncoded())
            self._storage.addObject(model, Request(Columns.Exclude("id")))

