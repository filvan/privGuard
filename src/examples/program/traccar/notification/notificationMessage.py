class NotificationMessage:


    def __init__(self, subject, body):
        self._subject = None
        self._body = None

        self._subject = subject
        self._body = body

    def getSubject(self):
        return self._subject

    def getBody(self):
        return self._body
