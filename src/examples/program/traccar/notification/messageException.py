class MessageException(Exception):

    def __init__(self, cause):
        super().__init__(cause)

    def __init__(self, message):
        super().__init__(message)
