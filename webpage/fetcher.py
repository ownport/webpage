# -*- coding: utf-8 -*-
#
#   fetcher.py
#

import io
import os
import re
import requests

from webpage.utils import gunzip


USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US)'
CODES_OK = requests.codes.ok

TEXT_MEDIA_TYPES = [
    'text/html', 'text/javascript', 'text/plain', 'text/xml',
    
    'application/atom+xml', 'application/json', 'application/javascript', 'application/rdf+xml',
    'application/rss+xml', 'application/soap+xml', 'application/xml', 
] 


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


    def fetch(self, url, to_file=None, check=False):
        ''' fetch url

        to_file - path and filename
        '''
        response = dict()
        
        try:
            if check is True:
                resp = requests.head(url, headers=self.headers, timeout=self.timeout)
            else:
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
                
            response['length'] = len(resp.content)

            if to_file:
                self.save(to_file, response)

        return response


    def save(self, filename, response):
        ''' save content for file
        '''
        content_disposition = response.get(u'content-disposition')
        if content_disposition:
            new_filename = ''.join(re.findall(
                                    r'attachment;\s*filename\s*=\s*[\"\']?(?P<filename>.*?)[\"\']?$', 
                                    content_disposition, re.I))
            if new_filename:
                filename = os.path.join(os.path.dirname(filename), new_filename)

        if filename and response[u'content-type'] in TEXT_MEDIA_TYPES:
            with io.open(filename, 'w', encoding='utf8') as f:
                f.write(response['content']) 
        elif filename:
            with io.open(filename, 'wb') as f:
                f.write(response['content']) 

        response['filename'] = filename


def fetch(url, headers={}, timeout=60., fetch_interval=30., to_file=None):
    ''' fetch url
    '''
    fetcher = Fetcher(headers=headers, timeout=timeout)
    return fetcher.fetch(url, to_file=to_file)



