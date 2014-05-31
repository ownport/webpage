# -*- coding: utf-8 -*-
#
#   fetcher.py
#

import io
import struct
import requests

from gzip import GzipFile
from cStringIO import StringIO

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US)'
CODES_OK = requests.codes.ok

TEXT_MEDIA_TYPES = [
    'text/html', 'text/javascript', 'text/plain', 'text/xml',
    
    'application/atom+xml', 'application/json', 'application/javascript', 'application/rdf+xml',
    'application/rss+xml', 'application/soap+xml', 'application/xml', 
] 


def gunzip(data):
    """Gunzip the given data and return as much data as possible.

    This is resilient to CRC checksum errors.
    """
    output = ''
    chunk = '.'
    with GzipFile(fileobj=StringIO(data)) as f: 
        while chunk:
            try:
                chunk = f.read(65536)
                output += chunk
            except (IOError, EOFError, struct.error), err:
                # complete only if there is some data, otherwise re-raise
                # see issue 87 about catching struct.error
                # some pages are quite small so output is '' and f.extrabuf
                # contains the whole page content
                if output or f.extrabuf:
                    output += f.extrabuf
                    break
                else:
                    raise
    return output


class Fetcher(object):


    def __init__(self, headers={}, timeout=60., fetch_interval=30.):
        ''' __init__
        
        xpath           - to select content
        headers['user-agent']
        timeout         - response timeout
        fetch_interval  - interval between fetch
        '''
        self.headers = dict()

        if headers.get('user-agent', None):
            headers['user-agent'] = USER_AGENT
        
        self.timeout = timeout
        self.fetch_interval = fetch_interval


    def check(self, url):
        ''' check URL by HEAD request
        '''    
        response = dict()
        
        try:
            resp = requests.head(url, headers=self.headers, timeout=self.timeout)
        
        except requests.exceptions.ConnectionError, err:
            response['status-code'] = -1
            response['error-msg'] = str(err.message)
            return response

        except requests.exceptions.Timeout, err:
            response['status-code'] = -2
            response['error-msg'] = 'Connection timeout'
            return response
            
        if resp.status_code == CODES_OK:
            response[u'status-code'] = resp.status_code
            response[u'content-type'] = resp.headers['content-type']
            response[u'url'] = unicode(resp.url)
            for name in resp.headers:
                response[unicode(name)] = resp.headers[name]

        return response


    def fetch(self, url, to_file=None):
        ''' fetch url

        to_file - path and filename
        '''
        response = dict()
        
        try:
            resp = requests.get(url, headers=self.headers, timeout=self.timeout)

        except requests.exceptions.ConnectionError, err:
            response['status-code'] = -1
            response['error-msg'] = str(err.message)
            return response

        except requests.exceptions.Timeout, err:
            response['status-code'] = -2
            response['error-msg'] = 'Connection timeout'
            return response

        if resp.status_code == CODES_OK:

            response[u'status-code'] = resp.status_code

            response[u'url'] = unicode(resp.url)
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
                response[u'content'] = gunzip(resp.content) 
                
            elif response[u'url'].endswith(u'.xml.gz'):
                response[u'content'] = gunzip(resp.content) 
            
            elif response[u'content-type'] in TEXT_MEDIA_TYPES:
                if resp.encoding:
                    if resp.encoding.lower() not in ['utf-8', 'utf8']:
                        resp.encoding = 'utf-8' 
                    response['encoding'] = resp.encoding
                response[u'content'] = resp.text

            else:
                response[u'content'] = resp.content

            if to_file and response[u'content-type'] in TEXT_MEDIA_TYPES:
                with io.open(to_file, 'w', encoding='utf8') as f:
                    f.write(response['content']) 
            elif to_file:
                with io.open(to_file, 'wb') as f:
                    f.write(response['content']) 

        return response

