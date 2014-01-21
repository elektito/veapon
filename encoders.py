class Encoder():
    def __init__(self, parent=None):
        # the parent of this Encoder, or `None` if this is the
        # parent. the `output` method sends the output to `self.cache`
        # if this is `None`, otherwise `self.parent.output` is called.
        self.parent = parent

        # generated output is stored in this variable if `self.parent`
        # is `None`.
        self.cache = b''

        # the list of sub-encoders. Encoder subclasses which use
        # sub-encoders will populate this list with the sub-encoders
        # they use. the default implementation of `feed` iterates
        # through these sub-encoders and feeds input to each encoder
        # until it is finished.
        self.encoders = []

        # the index of the current sub-encoder in `self.encoders`
        # being used for encoding.
        self.curEncoder = 0

    def feed(self, data):
        '''Any data to be encoded is sent to this method.

        This is the default implementation of the `feed` method for
        encoders which use a number of sub-encoders. It iteratively
        calls the sub-encoders (specified in the self.encoders
        variable).

        The `feed` method should return the rest of the data to be
        processed. If everything is processed b'' should be returned
        and if nothing is processed, `data` argument itself should be
        returned.

        Standalone encoders should override this.

        '''
        if type(data) != bytes:
            raise TypeError

        if len(self.encoders) == 0:
            return data

        rest = data
        while rest != b'':
            rest = self.encoders[self.curEncoder].feed(rest)

            self.curEncoder += 1
            self.curEncoder %= len(self.encoders)

    def output(self, data):
        '''This method should be called by the `feed` method. It saves some
        generated output in the main encoder's cache. The main encoder
        is the encoder with no parent.

        '''
        if self.parent == None:
            self.cache += data
        else:
            self.parent.output(data)

    def getOutput(self):
        '''Returns the output genereated so far without discarding the cache.

        '''
        return self.cache if self.parent == None else self.parent.cache

    def popOutput(self):
        '''Returns the output generated so far and discards the cache.

        '''
        if self.parent == None:
            ret = self.cache
            self.cache = b''
            return ret
        else:
            return self.parent.popOutput()

class HttpRequestLineEncoder(Encoder):
    class InvalidHttpVerbError(Exception):
        pass

    def __init__(self, verb=None, parent=None):
        super(HttpRequestLineEncoder, self).__init__(parent)
        self.verb = ''
