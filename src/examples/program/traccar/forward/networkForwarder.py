from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys

class NetworkForwarder:

    _LOGGER = "LoggerFactory.getLogger(NetworkForwarder.class)"

    def __init__(self, config):

        self._destination = None
        self._connectionUdp = None
        self._connectionsTcp = {}

        self._destination = "InetAddress.getByName(config.getString(Keys.SERVER_FORWARD))"
        self._connectionUdp = "DatagramSocket()"

    def forward(self, source, port, datagram, data):
        try:
            if datagram:
                self._connectionUdp.send("DatagramPacket(data, len(data), self._destination, port)")
            else:
                connectionTcp = self._connectionsTcp[source]
                if connectionTcp is None or connectionTcp.isClosed():
                    connectionTcp = "Socket(self._destination, port)"
                    self._connectionsTcp[source] = connectionTcp
                connectionTcp.getOutputStream().write(data)
        except Exception as e:
            NetworkForwarder._LOGGER.warn("Network forwarding error", e)

    def disconnect(self, source):
        connectionTcp = self._connectionsTcp.pop(source)
        if connectionTcp is not None:
            try:
                connectionTcp.close()
            except Exception as e:
                NetworkForwarder._LOGGER.warn("Connection close error", e)
