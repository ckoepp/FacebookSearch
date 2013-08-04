# -*- coding: utf-8 -*-

from .FacebookSearchOrder import FacebookSearchOrder
from .FacebookSearchException import FacebookSearchException
from .utils import py3k
import requests

try: from urllib.parse import parse_qs # python3
except ImportError: from urlparse import parse_qs # python2

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
        if isinstance(client_secret, str if py3k else basestring) and isinstance(client_id, str if py3k else basestring):
            self.__access_token = self.queryAccessToken(client_id, client_secret)
        elif isinstance(access_token, str if py3k else basestring):
            self.__access_token = access_token
            if verify:
                self.validateAccessToken(self.__access_token)
        else:
            raise FacebookSearchException(1000)

        self.__headers = None
        self.__response = None
        self.__last_query = None
        self.__query = None

    def queryAccessToken(self, client_id, client_secret):
        """ Tries to fetch and return an access token by transmitting a client's ID and secret to Fracebook Graph """
        response = self.sendQuery(self._generate_token_url + '?client_id=%s&client_secret=%s&grant_type=client_credentials' % (client_id, client_secret), addToken=False)
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

    def getLastQuery(self):
        """ Returns last query string passed to the Graph API """

    def sendQuery(self, query, addToken=True):
        """ Adds a token if needed to a given query and returns response either as json-parsed dict or string """
        self.__last_query = query

        if addToken:
            self.__last_query += '&access_token=%s' % self.__access_token

        r = requests.get(self.__last_query)
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
                # ...and sometimes there is even no error code at all included in error messages *double d'oh*
                code = 0 if not self.__response['error'].get('code') else self.__response['error']['code']

                raise FacebookSearchException(code, "%s: %s" % (self.__response['error']['type'], self.__response['error']['message']))

        except Exception as e:

            print("EXCEPTION!!!")
            # re-raise exception as one of ours, if it was raised because of an json error returned by Graph API
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
        """ Creates a query string through a given FacebookSearchOrder object and sends a query to Facebook Graph with added postfix string """
        if not isinstance(order, FacebookSearchOrder):
            raise FacebookSearchException(1002)
        self.__query = order.createSearchQuery()
        return self.sendQuery(self._search_url + self.__query)

    def searchGraphIterable(self, order):
        """ Starts an iterable search through a given FacebookSearchOrder object and returns itself """
        self.searchGraph(order)
        return self

    def isPreviousPage(self):
        """ Returns true in case there are more results within Graph API or false if there aren't """
        if self.__response.get('paging') and self.__response['paging'].get('previous'):
            return True
        return False

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

        # Graph Search only supports time-based pagination - don't ask me why
        # see: https://developers.facebook.com/docs/reference/api/pagination/

        # empty results? FB got it all - it's horrible...
        # see: https://developers.facebook.com/blog/post/478/
        while self.isPreviousPage():
            last_ts = parse_qs(self.__response['paging']['next'])['until'][0]
            self.sendQuery(self._search_url + self.__query + '&until=%s' % last_ts)

            if len(self.__response['data']) > 0:
                self.__nextObject = 1
                return self.__response['data'][0]

            # Sometimes response of Graph API is just "{ data [] }" - this is f*cking stupid behavior of an API. Thanks a lot Facebook!
            # see: http://stackoverflow.com/questions/13299004/facebook-graph-api-search-returning-empty-data
            else:
                break

        raise StopIteration
