from .FacebookSearchOrder import FacebookSearchOrder
from .FacebookSearchException import FacebookSearchException
from .utils import py3k

import requests

class FacebookSearch(object):
    _base_url = 'https://graph.facebook.com/'
    _generate_token_url = _base_url + 'oauth/access_token'


    exceptions = {
            200 : "All perfect - too perfect!"
            }

    def __init__(self, client_id = None, client_secret = None, access_token = None):

        if isinstance(client_secret, basestring if py3k else str) and isinstance(client_id, basestring if py3k str):
            self.__access_token = self.queryAccessToken(client_id, client_secret)
        elif isinstance(access_token, basestring if py3k else str):
            self.__access_token = access_token

    def queryAccessToken(self, client_id, client_secret):
        r = requests.get(self._generate_token_url + '?client_id=%s&client_secret=%s&grant_type=client_credentials')
        print(r.text)


    def checkHTTPStatus(self, http_status):
        if http_status in exceptions:
            raise FacebookSearchException(http_status, exceptions[http_status])


