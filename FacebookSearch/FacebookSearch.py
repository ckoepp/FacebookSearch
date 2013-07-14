# -*- coding: utf-8 -*-

from .FacebookSearchOrder import FacebookSearchOrder
from .FacebookSearchException import FacebookSearchException
from .utils import py3k

import requests

class FacebookSearch(object):
    """
    This class actually performs querys to the Facebook Graph API
    """

    _base_url = 'https://graph.facebook.com/'
    _generate_token_url = _base_url + 'oauth/access_token'
    _verify_url = _base_url + 'app?fields=id'
    _search_url = _base_url + 'search'

    # HTTP error codes do exist but are not documented by Facebook *doh*
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

    def sendQuery(self, query):
        """ Sends a given query and returns response either as json-parsed dict or string """
        r = requests.get(query)

        status = r.status_code
        if status in self.exceptions:
            raise FacebookSearchException(status, self.exceptions[status])

        self.__headers = r.headers

        # Again: DON'T ASK - Graph should be a RESTful API but access-tokens are returned as non-json objects for example *d'oh*
        try:
            self.__response = r.json()

            # json error returned? Raise exception
            if not self.__response.get('error'):
                return self.__response
            else:
                raise FacebookSearchException(self.__response['error']['code'], "%s: %s" % (self.__response['error']['type'], self.__response['error']['message']))

        except Exception as e:

            # re-raise exception if it was raised because of an json error returned by Graph API
            if isinstance(e, FacebookSearchException):
                raise e
            self.__response = r.text
            return self.__response

    def validateAccessToken(self, token):
        """ Validates a given access token against Facebook Graph. Returns True in case of success or False in other cases """
        response = self.sendQuery(self._verify_url + '&access_token=%s' %  token)

        # User Token
        if token.find('|') < 0:
            if response['id'].isdigit():
                return True
            return False

        # App Token
        if self.__access_token[0:len(response['id'])] == response['id']:
            return True
        return False

    def searchGraph(self, order):
        """ Creates a query string through a given FacebookSearchOrder object and sends a query to Facebook Graph """
        if not isinstance(order, FacebookSearchOrder):
            raise FacebookSearchException(1002)
        return self.sendQuery(self._search_url + order.createSearchQuery() + '&access_token=%s' % self.__access_token)

    def searchGraphIterable(self, order):
        """ Starts an iterable search through a given FacebookSearchOrder object and returns itself """
        self.searchGraph(order)
        return self


    # Iterator
    def __iter__(self):
        if not self.__response:
            raise FacebookSearchException(1003)
        self.__nextObject = 0
        return self

    def next(self):
        """ Python2 version of __next__() """
        return self.__next__()

    def __next__(self):
        if self.__nextObject < len(self.__response['data']):
            self.__nextObject += 1
            return self.__response['data'][self.__nextObject-1]
        else:
            raise StopIteration
