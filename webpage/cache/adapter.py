from requests.adapters import HTTPAdapter

from logging import getLogger
log = getLogger(__name__)

from cache import HTTPCache


class CachingHTTPAdapter(HTTPAdapter):
    ''' A HTTP-caching-aware Transport Adapter for Python Requests. The central
    portion of the API.
    '''
    def __init__(self, cache=None, **kwargs):

        log.debug('CachingHTTPAdapter.__init__(), cache: %s, kwargs: %s' % (cache, kwargs))
        super(CachingHTTPAdapter, self).__init__(**kwargs)

        #: The HTTP Cache backing the adapter.
        if cache: 
            self.cache = cache
        else:
            raise RuntimeError('Error! Cache backend is not defined')


    def send(self, request, **kwargs):
        ''' Sends a PreparedRequest object, respecting RFC 2616's rules about HTTP
        caching. Returns a Response object that may have been cached.

        :param request: The Requests :class:`PreparedRequest <PreparedRequest>` object to send.
        '''
        log.debug('CachingHTTPAdapter.send(), url: %s' % request.url)
        cached_resp = self.cache.retrieve(request)

        if cached_resp is not None:
            log.info('URL is available in cache, %s' % request.url)
            return cached_resp
        else:
            return super(CachingHTTPAdapter, self).send(request, **kwargs)


    def build_response(self, request, response):
        ''' Builds a Response object from a urllib3 response. May involve returning
        a cached Response.

        :param request: The Requests :class:`PreparedRequest <PreparedRequest>` object sent.
        :param response: The urllib3 response.
        '''
        log.debug('CachingHTTPAdapter.build_response(), url: %s' % request.url)
        resp = super(CachingHTTPAdapter, self).build_response(request, response)

        if resp.status_code == 304:
            resp = self.cache.handle_304(resp)
        else:
            self.cache.store(resp)

        return resp
