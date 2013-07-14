class FacebookSearchException(object):

    _error_codes = [
            1000 : "Default exception",
            ]

    def __init__(self, code, msg = None):
        self.code = code
        if msg:
            self.message = msg
        else:
            self.message = self._error_codes.get(code)

    def __str__(self):
        return "Error %i: %s" % (self.code, self.message)
