import base64
import sys
from datetime import date
from plistlib import Data

from kafka.metrics.stats.rate import TimeUnit

from src.examples.program.traccar.storage.storageException import StorageException

class TokenManager:

    _DEFAULT_EXPIRATION_DAYS = 7


    class Data:

        def __init__(self):

            self._userId = 0
            self._expiration = None


    def __init__(self, objectMapper, cryptoManager):

        self._objectMapper = None
        self._cryptoManager = None

        self._objectMapper = objectMapper
        self._cryptoManager = cryptoManager

    def generateToken(self, userId):
        return self.generateToken(userId, None)

    def generateToken(self, userId, expiration):
        data = Data()
        data.userId = userId
        if expiration is not None:
            data.expiration = expiration
        else:
            data.expiration = date(sys.currentTimeMillis() + TimeUnit.DAYS.toMillis(TokenManager._DEFAULT_EXPIRATION_DAYS))
        encoded = self._objectMapper.writeValueAsBytes(data)
        return base64.encodeBase64URLSafeString(self._cryptoManager.sign(encoded))

    def verifyToken(self, token):
        encoded = self._cryptoManager.verify(base64.decodeBase64(token))
        data = self._objectMapper.readValue(encoded, Data.__class__)
        if data.expiration.before(date()):
            raise Exception("Token has expired")
        return data.userId
