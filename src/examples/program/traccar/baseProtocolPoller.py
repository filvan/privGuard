from kafka.metrics.stats.rate import TimeUnit


class BaseProtocolPoller():


    def __init__(self, interval):

        self._interval = 0
        self._timeout = None

        self._interval = interval

    def sendRequest(self, channel, remoteAddress):
        pass

    def channelActive(self, ctx):
        super().channelActive(ctx)
        if self._interval > 0:
            self._timeout = ctx.executor().scheduleAtFixedRate(lambda : self.sendRequest(ctx.channel(), ctx.channel().remoteAddress()), 0, self._interval, TimeUnit.SECONDS)

    def channelInactive(self, ctx):
        super().channelInactive(ctx)
        if self._timeout is not None:
            self._timeout.cancel(False)
            self._timeout = None
