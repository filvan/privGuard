class StorageException(Exception):
    def __init__(self, message=None, cause=None):
        super().__init__(message, cause)
