# -*- coding: utf-8 -*-
#
import io
import os
import json
import time
import utils
import codecs

from datetime import datetime

from logging import getLogger
log = getLogger(__name__)

from requests.models import Response
from requests.structures import CaseInsensitiveDict


# RFC 2616 specifies that we can cache 200 OK, 203 Non Authoritative,
# 206 Partial Content, 300 Multiple Choices, 301 Moved Permanently and
# 410 Gone responses. We don't cache 206s at the moment because we
# don't handle Range and Content-Range headers.
CACHEABLE_RCS = (200, 203, 300, 301, 410)

# Cacheable verbs.
CACHEABLE_VERBS = ('GET', 'HEAD', 'OPTIONS')

# Some verbs MUST invalidate the resource in the cache, according to RFC 2616.
# If we send one of these, or any verb we don't recognise, invalidate the
# cache entry for that URL. As it happens, these are also the cacheable
# verbs. That works out well for us.
NON_INVALIDATING_VERBS = CACHEABLE_VERBS


class HTTPCache(object):

    def __init__(self, path, expiration_time=-1):

        log.debug('HTTPCache.__init__(), path: %s' % path)
        super(HTTPCache, self).__init__()

        if not path:
            raise RuntimeError('Error! The path to cache is not defined, %s' % path)
        # Make sure the path exists
        try:
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(path)
        except (IOError, OSError):
            raise RuntimeError('Error! Cannot create cache directory, %s' % path)

        self.path = path


    def _fn(self, name):

        return utils.offline_link(name, path=self.path)


    def retrieve(self, request):

        filename = self._fn(request.url)
        resp = Response()

        headers = utils.read('%s.metadata' % filename)
        if headers:
            try:
                headers = CaseInsensitiveDict(json.loads(headers))
            except ValueError:
                return None
            headers['x-cache'] = 'HIT from %s' % self.__class__.__name__
            resp.url = headers.pop('url', None)
            resp.status_code = headers.pop('status-code', None)
            resp.encoding = headers.pop('encoding', None)
            resp.headers = headers
            resp._content = utils.read(filename)
            return resp
        else:
            return None
            

    def store(self, response):

        headers = dict(response.headers.copy())
        headers['url'] = response.url
        if response.encoding:
            headers['encoding'] = response.encoding.lower()
        headers['status-code'] = int(response.status_code)

        filename = self._fn(response.url)
        utils.save('%s.metadata' % filename, 
                        content=json.dumps(headers, indent=4, sort_keys=True) + '\n')
        utils.save(filename, 
                        headers=response.headers, 
                        content=response.content)
        return True


class URLRulesHTTPCache(HTTPCache):
    ''' HTTP cache based on URL rules
    '''
    def __init__(self, urls={}, path=None, expiration_time=-1):
        ''' __init__

        - urls              - list of URL patters
        - path              - where files will be stores
        - expiration-time   - expiration time in seconds
        '''
        super(URLRulesHTTPCache, self).__init__(path=path, expiration_time=expiration_time)
        if isinstance(urls, (list, set, tuple)):
            self._urls = list(urls)
        else:
            raise RuntimeError('Error! URLs are not defined')


    def retrieve(self, request):
        ''' retrieve
        '''
        if request.url not in self._urls:
            return None
        return super(URLRulesHTTPCache, self).retrieve(request)


    def store(self, response):
        ''' store
        '''
        if not response or not isinstance(response, Response):
            return False

        if response.url not in self._urls:
            return False
            
        return super(URLRulesHTTPCache, self).store(response)




