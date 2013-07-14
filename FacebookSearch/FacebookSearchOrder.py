from .FacebookSearchException import FacebookSearchException
from .utils import py3k

try: from urllib.parse import parse_qs, quote_plus, unquote # python3
except ImportError: from urlparse import parse_qs; from urllib import quote_plus, unquote #python2

class FacebookSearchOrder(object):
    def __init__(self):
        self.__keywords = []
        self.__parameters = {}
        self.__parameters.update({ 'limit' : '500' })
        self.__fields = {}

    def createSearchQuery(self):
        """ Creates and returns a query string based on the arguments and keywords set so far """
        querystr = '?'

        # keywords
        querystr += 'q='
        args = self.__keywords
        for arg in args:
            arg = quote_plus(arg)
        querystr += '+'.join(args)

        # included fields
        if len(self.__fields) > 0:
            querystr += '&fields='
            querystr += ','.join(self.__fields)

        # additional arguments
        for key, value in self.__parameters.items():
            querystr += '&%s=%s' % (quote_plus(key), quote_plus(value) if not key == 'center' else value)

        return querystr

    def setSearchType(self, search_type):
        """ Sets a search type """
        if isinstance(search_type, basestring if py3k else str):
            self.__parameters['type'] = search_type
        else:
            raise FacebookSearchException(1005)

    def setGeolocationType(self, search_type, lat, lon, distance=None):
        """ Sets a type containing a geolocation and an optional distance parameter """
        if not isinstance(search_type, basestring if py3k else str):
            raise FacebookSearchException(1005)
        if not isinstance(lat, float) and isinstance(lon, float):
            raise FacebookSearchException(1006)
        if not isinstance(distance, int if py3k else (long, int)):
            raise FacebookSearchException(1007)

        if distance:
                self.__parameters['distance'] = '%s' % distance

        self.__parameters['type'] = search_type
        self.__parameters['center'] = "%s,%s" % (lat, lon)

    def setPlaceID(self, place_id):
        """ Sets a given place_id as paramater """
        if isinstance(place_id, int if py3k else (long, int)):
            self.__paramters['place'] = '%s' % place_id
        else:
            raise FacebookSearchException(1007)

    def setIncludedFields(self, fields):
        """ Sets given list or string of fields to be exclusivly included in response """
        if isinstance(fields, basestring if py3k else str):
            self.__fields = [ fields ]
        elif isinstance(fields, list):
            self.__fields = fields
        else:
            raise FacebookSearchException(1004)

    def addIncludedFields(self, fields):
        """ Adds given list or string of fields to be exclusivly included in response """
        if isinstance(fields, basestring if py3k else str):
            self.__fields.append(fields)
        elif isinstance(fields, list):
            self.__fields += fields
        else:
            raise FacebookSearchException(1004)

    def setKeywords(self, words):
        """ Sets given list or string of fields as keywords """
        if isinstance(words, basestring if py3k else str):
            self.__keywords = [ words ]
        elif isinstance(words, list):
            self.__keywords = words
        else:
            raise FacebookSearchException(1004)

    def addKeywords(self, words):
        """ Adds given list or string of fields to keywords """
        if isinstance(words, basestring if py3k else str):
            self.__keywords.append(words)
        elif isinstance(words, list):
            self.__keywords += words
        else:
            raise FacebookSearchException(1004)

