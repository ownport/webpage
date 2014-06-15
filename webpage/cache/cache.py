# -*- coding: utf-8 -*-
#
import os
import json
import time
import utils
import codecs

from datetime import datetime, timedelta

from logging import getLogger
log = getLogger(__name__)

from requests import Response


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

    def __init__(self, path):

        log.debug('HTTPCache.__init__(), path: %s' % path)
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


    def handle_304(self, response):
        ''' Given a 304 response, retrieves the cached entry. This unconditionally
        returns the cached entry, so it can be used when the 'intelligent'
        behaviour of retrieve() is not desired.

        Returns None if there is no entry in the cache.

        :param response: The 304 response to find the cached entry for. Should be 
                        a Requests :class:`Response <Response>`.
        '''
        log.debug('HTTPCache.handle_304(), url: %s' % response.url)
        try:
            filename = self._fn(response.url)
            cached_response = self._get[filename]
        except KeyError:
            cached_response = None

        return cached_response


    def retrieve(self, request):

        log.debug('HTTPCache.retrieve(), url: %s' % request.url)
        url = request.url

        if request.method not in NON_INVALIDATING_VERBS:
            return None

        cached_response = self._get(self._fn(url))
        if not cached_response:
            return None

        if cached_response.headers.get('expiry') is None:
            # We have no explicit expiry time, so we weren't instructed to
            # cache. Add an 'If-Modified-Since' header.
            creation = datetime.fromtimestamp(cached_response.headers.get('creation'))
            header = utils.build_date_header(creation)
            request.headers['If-Modified-Since'] = header
        else:
            # We have an explicit expiry time. If we're earlier than the expiry
            # time, return the response.
            now = datetime.utcnow()

            if now <= datetime.fromtimestamp(cached_response.headers.get('expiry')):
                return_response = cached_response

        return cached_response


    def store(self, response):

        log.debug('HTTPCache.store(), url: %s' % response.url)
        if response.status_code not in CACHEABLE_RCS:
            return False

        if response.request.method not in CACHEABLE_VERBS:
            return False

        url = response.url
        now = datetime.utcnow()

        # Get the value of the 'Date' header, if it exists. If it doesn't, just
        # use now.
        creation = utils.date_header_or_default('Date', now, response)

        # Get the value of the 'Cache-Control' header, if it exists.
        cc = response.headers.get('Cache-Control', None)
        if cc is not None:
            expiry = utils.expires_from_cache_control(cc, now)

            # If the above returns None, we are explicitly instructed not to
            # cache this.
            if expiry is None:
                return False

        # Get the value of the 'Expires' header, if it exists, and if we don't
        # have anything from the 'Cache-Control' header.
        if cc is None:
            expiry = utils.date_header_or_default('Expires', None, response)

        # If the expiry date is earlier or the same as the Date header, don't
        # cache the response at all.
        if expiry is not None and expiry <= creation:
            return False

        # If there's a query portion of the url and it's a GET, don't cache
        # this unless explicitly instructed to.
        if expiry is None and response.request.method == 'GET':
            if utils.url_contains_query(url):
                return False

        headers = dict(response.headers.copy())
        headers['url'] = response.url
        if expiry:
            headers['expiry'] = int(expiry.strftime('%s'))
        if creation:
            headers['creation'] = int(creation.strftime('%s'))
        headers['encoding'] = response.encoding.lower()
        headers['status-code'] = int(response.status_code)

        filename = self._fn(response.url)
        self._save_file('%s.metadata' % filename, 
                        json.dumps(headers, indent=4, sort_keys=True) + '\n')
        self._save_file(filename, response.content)


    def _get(self, filename):

        resp = Response()

        headers = self._read_file('%s.metadata' % filename)
        if headers:
            headers = json.loads(headers)
            resp.url = headers.pop('url', None)
            resp.status_code = headers.pop('status-code', None)
            resp.encoding = headers.pop('encoding', None)
            resp.headers = headers
            resp._content = self._read_file(filename)
            return resp
        else:
            return None

    def _read_file(self, filename):

        if not os.path.exists(filename):
            return None

        with codecs.open(filename, 'r', encoding='utf8') as fh:
            return fh.read()


    def _save_file(self, filename, content):

        with codecs.open(filename, 'w', encoding='utf8') as fh:
            fh.write(content)    
