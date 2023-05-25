class BaseFrameDecoder():

    def decode(self, ctx, in_, out):
        decoded = self.decode(ctx,ctx.channel() if ctx is not None else None, in_)
        if decoded is not None:
            out.append(decoded)

    def decode(self, ctx, channel, buf):
        pass
