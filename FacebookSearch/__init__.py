# -*- coding: utf-8 -*-

__title__ = 'FacebookSearch'
__version__ = '0.0.1'
__author__ = 'Christian Koepp, Norbert Wiedermann'
__license__ = 'MIT'
__copyright__ = 'Copyright 2013 Christian Koepp and Norbert Wiedermann'

from .FacebookSearch import FacebookSearch
from .FacebookSearchOrder import FacebookSearchOrder
from .FacebookSearchException import FacebookSearchException
from .utils import py3k

# ToDo
class SEARCH_TYPES(type):
    _types = {
            'POST'     : 'post',
            'USER'     : 'user',
            'PAGE'     : 'page',
            'EVENT'    : 'event',
            'GROUP'    : 'group',
            'PLACE'    : 'place',
            'CHECKIN'  : 'checkin',
            'LOCATION' : 'location',
        }

    def __getattr__(cls, key):
        if key in self._types.keys():
            return self._types[key.upper()]
        else:
            raise AttributeError(key)
