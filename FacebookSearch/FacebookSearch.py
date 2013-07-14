from .FacebookSearchOrder import FacebookSearchOrder
from .FacebookSearchException import FacebookSearchException
from .utils import py3k

import requests

class FacebookSearch(object):
    _base_url = 'https://graph.facebook.com/'
    _generate_token_url = _base_url + 'oauth/access_token'
    _verify_url = _base_url + 'app?fields=id'
    _search_url = _base_url + 'search'


    exceptions = {
            400 : "The request could not be fulfilled",
            }

    def __init__(self, client_id = None, client_secret = None, access_token = None, verify=True):
        """ Constructor """
        if isinstance(client_secret, basestring if py3k else str) and isinstance(client_id, basestring if py3k else str):
            self.__access_token = self.queryAccessToken(client_id, client_secret)
        elif isinstance(access_token, basestring if py3k else str):
            self.__access_token = access_token
            if verify:
                self.validateAccessToken(self.__access_token)
        else:
            raise FacebookSearchException(1000)

        self.__headers = None
        self.__response = None

    def queryAccessToken(self, client_id, client_secret):
        """ Tries to fetch and return an access token by transmitting a client's ID and secret to Fracebook Graph """
        response = self.sendQuery(self._generate_token_url + '?client_id=%s&client_secret=%s&grant_type=client_credentials' % (client_id, client_secret))
        args = response.split('=')
        if args[0] == 'access_token':
            return args[1]
        else:
            raise FacebookSearchException(1001)

    def getHeaders(self):
        """ Returns list of headers of last query """
        return self.__headers

    def getResponse(self):
        """ Returns the full response of last query """
        return self.__response

    def sendQuery(self, query, json=False):
        """ Sends a given query and returns response either as json-parsed dict or string """
        r = requests.get(query)

        status = r.status_code
        if status in self.exceptions:
            raise FacebookSearchException(status, self.exceptions[status])

        self.__headers = r.headers

        if json:
            self.__response = r.json()
            return self.__response
        else:
            self.__response = r.text
            return self.__response

    def validateAccessToken(self, token):
        """ Validates a given access token against Facebook Graph. Returns True in case of success or False in other cases """
        response = self.sendQuery(self._verify_url + '&access_token=%s' %  token, json=True)
        if self.__access_token[0:len(response['id'])] == response['id']:
            return True
        else:
            return False

    def searchGraph(self, order):
        """ Creates a query string through a given FacebookSearchOrder object and sends a query to Facebook Graph """
        if not isinstance(order, FacebookSearchOrder):
            raise FacebookSearchException(1002)
        return self.sendQuery(self._search_url + order.createSearchQuery() + '&access_token=%s' % self.__access_token, json=True)

    def searchGraphIterable(self, order):
        """ Starts an iterable search through a given FacebookSearchOrder object and returns itself """
        self.searchGraph(order)
        print(self.__response['paging'])
        return self


    # Iterator
    def __iter__(self):
        if not self.__response:
            raise FacebookSearchException(1003)
        self.__nxt = 0
        return self

    def next(self):
        """ Python2 version of __next__() """
        return self.__next__()

    def __next__(self):
        if self.__nxt < len(self.__response['data']):
            self.__nxt += 1
            return self.__response['data'][self.__nxt-1]
        else:
            raise StopIteration
