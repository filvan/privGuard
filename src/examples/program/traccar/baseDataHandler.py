from src.examples.program.traccar.model.position import Position
class BaseDataHandler():

    def channelRead(self, ctx, msg):
        if isinstance(msg, Position):
            position = self.handlePosition(msg)
            if position is not None:
                ctx.fireChannelRead(position)
        else:
            super().channelRead(ctx, msg)

    def handlePosition(self, position):
        pass
