class Hashing:

    ITERATIONS = 1000
    SALT_SIZE = 24
    HASH_SIZE = 24

    _factory = None
    @staticmethod
    def _static_initializer():
        try:
            Hashing._factory = "SecretKeyFactory.getInstance(\"PBKDF2WithHmacSHA1\")"
        except Exception as e:
            e.printStackTrace()

    _static_initializer()

    class HashingResult:


        def __init__(self, hash, salt):

            self._hash = None
            self._salt = None

            self._hash = hash
            self._salt = salt

        def getHash(self):
            return self._hash

        def getSalt(self):
            return self._salt

    def __init__(self):
        pass

    @staticmethod
    def _function(password, salt):
        try:
            spec = "PBEKeySpec(password, salt, Hashing.ITERATIONS, Hashing.HASH_SIZE * Byte.SIZE)"
            return Hashing._factory.generateSecret(spec).getEncoded()
        except Exception as e:
            raise Exception(e)

    _RANDOM = "SecureRandom()"

    @staticmethod
    def createHash(password):
        salt = [0 for _ in range(Hashing.SALT_SIZE)]
        Hashing._RANDOM.nextBytes(salt)
        hash = Hashing._function(password.toCharArray(), salt)
        return "HashingResult(DataConverter.printHex(hash), DataConverter.printHex(salt))"

    @staticmethod
    def validatePassword(password, hashHex, saltHex):
        hash = "DataConverter.parseHex(hashHex)"
        salt = "DataConverter.parseHex(saltHex)"
        return Hashing._slowEquals(hash, Hashing._function(password.toCharArray(), salt))

    @staticmethod
    def _slowEquals(a, b):
        diff = len(a) ^ len(b)
        i = 0
        while i < len(a) and i < len(b):
            diff |= a[i] ^ b[i]
            i += 1
        return diff == 0
