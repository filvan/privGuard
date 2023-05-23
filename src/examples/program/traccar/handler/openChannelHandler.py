from src.examples.program.traccar.trackerConnector import TrackerConnector

class OpenChannelHandler():


    def __init__(self, connector):

        self._connector = None

        self._connector = connector

    def channelActive(self, ctx):
        super().channelActive(ctx)
        self._connector.getChannelGroup().add(ctx.channel())

    def channelInactive(self, ctx):
        super().channelInactive(ctx)
        self._connector.getChannelGroup().remove(ctx.channel())
