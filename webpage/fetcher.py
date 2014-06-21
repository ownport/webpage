# -*- coding: utf-8 -*-
#
#   fetcher.py
#

import io
import os
import re
import hashlib
import requests

from logging import getLogger
log = getLogger(__name__)

import utils
from adapter import CachingHTTPAdapter


USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US)'
CODES_OK = requests.codes.ok

TEXT_MEDIA_TYPES = [
    'text/html', 'text/javascript', 'text/plain', 'text/xml',
    
    'application/atom+xml', 'application/json', 'application/javascript', 'application/rdf+xml',
    'application/rss+xml', 'application/soap+xml', 'application/xml', 
] 


class Fetcher(object):


    def __init__(self, headers={}, timeout=60., fetch_interval=30., caching_adapter=None):
        ''' __init__
        
        - headers: {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US)'}
        - timeout: response timeout
        - fetch_interval: interval between fetch
        - cc_adapter: cachecontrol.CacheControlAdapter 
        '''
 
        self.session = requests.Session()
        self.session.headers.update({'user-agent': USER_AGENT})
        if headers:
            self.session.headers.update(headers)

        self.timeout = timeout

        # TODO, fetch_interval is not used in the current implementation
        self.fetch_interval = fetch_interval

        # Cache Control
        if caching_adapter and isinstance(caching_adapter, CachingHTTPAdapter):
            self.session.mount('http://', caching_adapter)
            self.session.mount('https://', caching_adapter)


    def fetch(self, url, to_file=None, check=False):
        ''' fetch url

        to_file - path and filename
        '''
        response = dict()
        
        try:
            if check is True:
                resp = self.session.head(url, timeout=self.timeout)
            else:
                resp = self.session.get(url, timeout=self.timeout)

        # In the event of a network problem (e.g. DNS failure, refused connection, etc)
        except requests.exceptions.ConnectionError, err:
            response['url'] = url
            response['status-code'] = -1
            response['error-msg'] = str(err.message)
            return response

        # If a request times out
        except requests.exceptions.Timeout, err:
            response['url'] = url
            response['status-code'] = -2
            response['error-msg'] = 'Connection timeout'
            return response

        # In the event of the rare invalid HTTP response
        except requests.exceptions.HTTPError:
            log.debug('Unhandled HTTPError exception, %s' % url)
            raise RuntimeError('Error! Unhandled HTTPError exception')

        # If a request exceeds the configured number of maximum redirections
        except requests.exceptions.TooManyRedirects:
            log.debug('Unhandled TooManyRedirects exception, %s' % url)
            raise RuntimeError('Error! Unhandled TooManyRedirects exception')

        response = self._handle_response(resp)
        if to_file:
            r = response.copy()
            content = r.pop('content', None)
            response['filename'] = utils.save(to_file, headers=r, content=content)

        return response


    def _handle_response(self, resp):
        ''' response handling
        '''
        response = dict()

        response[u'status-code'] = resp.status_code
        response[u'url'] = unicode(resp.url)
        response[u'url-hash'] = hashlib.sha1(response[u'url']).hexdigest()

        if resp.status_code == CODES_OK:

            for name in resp.headers:
                response[unicode(name)] = unicode(resp.headers[name])

            # content-type
            content_type = [p.strip() for p in response[u'content-type'].split(';')]
            if len(content_type) > 1:
                response[u'content-type'] = content_type[0]
                response[u'content-type-parameters'] = content_type[1].lower()
            else:
                response[u'content-type'] = resp.headers['content-type']

            # handle compressed content
            if response[u'content-type'] in ('application/x-gzip', 'application/gzip'):
                response[u'content'] = utils.gunzip(resp.content) 
                
            elif response[u'url'].endswith(u'.xml.gz'):
                response[u'content'] = utils.gunzip(resp.content) 
            
            elif response[u'content-type'] in TEXT_MEDIA_TYPES:

                if resp.encoding:
                    if resp.encoding.lower() not in ['utf-8', 'utf8']:
                        resp.encoding = 'utf-8' 
                    response[u'encoding'] = resp.encoding
                if isinstance(resp.content, unicode):
                    response[u'content'] = resp.content
                else:
                    response[u'content'] = resp.text

            else:
                response[u'content'] = resp.content
            
            response[u'content-hash'] = hashlib.sha1(resp.content).hexdigest()  
            response[u'content-length'] = len(resp.content)

        return response


def fetch(url, headers={}, timeout=60., to_file=None):
    ''' fetch url
    '''
    fetcher = Fetcher(headers=headers, timeout=timeout)
    return fetcher.fetch(url, to_file=to_file)


def check(url, headers={}, timeout=60.):
    ''' check url
    '''
    fetcher = Fetcher(headers=headers, timeout=timeout)
    return fetcher.fetch(url, check=True, to_file=to_file)


