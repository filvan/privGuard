class NetworkUtil:

    def __init__(self):
        pass

    @staticmethod
    def session(channel):
        transport = 'U' if isinstance(channel, DatagramChannel) else 'T'
        return transport + channel.id().asShortText()
