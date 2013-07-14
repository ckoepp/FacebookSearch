class FacebookSearchException(Exception):

    _error_codes = {
            1000 : "No access token or no client ID/secret tuple found",
            1001 : "Couldn't fetch a valid access token from Facebook API",
            1002 : "Not a valid FacebookSearchOrder object",
            1003 : "No results available",
            }

    def __init__(self, code, msg = None):
        self.code = code
        if msg:
            self.message = msg
        else:
            self.message = self._error_codes.get(code)

    def __str__(self):
        return "Error %i: %s" % (self.code, self.message)
