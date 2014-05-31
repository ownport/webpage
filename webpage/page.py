#
#   Simple web archive format
#

import io
import os
import re
import json
import fetcher
import tempfile

from os.path import basename
from urlparse import urlparse

from parser import Parser
from template import PageTemplate


USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US)'


class Webpage(object):
    ''' Simple Web page archiver
    '''
    def __init__(self, url=None, path=None, template=None, rules={}):
        ''' __init__

        url     - webpage url
        path    - drectory path where files will be stored
        '''
        self.url = url
        self.fetcher = fetcher.Fetcher(headers={'user-agent': USER_AGENT})
        self.metadata = dict()
        self.resources = dict()
        self.content = None
        self.path = path

        self.template = None
        if template:
            self.template = PageTemplate(template)

        self.rules = rules


    def is_available(self):
        ''' return True if page is available
        '''
        response = self.fetcher.check(self.url)
        if response.get('status-code', None) == fetcher.CODES_OK:
            return True
        return False


    def fetch_page(self):
        ''' fetch webpage
        '''
        response = self.fetcher.fetch(self.url)
        if response.get('status-code', None) == fetcher.CODES_OK:
            self.content = response.pop('content')
            self.metadata = response
        else:
            raise RuntimeError('Error! Web page is not available: %s' % self.url)


    def fetch_resources(self, pattern=None):
        ''' fetch resources (images, css, javascript, video, ...)
        '''
        if not pattern:
            raise RuntimeError('Error! The pattern is not defined')

        if not self.content:
            self.fetch_page()

        pattern = re.compile(pattern)
        path = os.path.join(self.path, 'files/')
        if not os.path.exists(path):
            os.makedirs(path)

        parser = Parser(self.url, self.content)
        for link in parser.extract_links():
            if pattern and pattern.search(link):
                
                parsed_url = urlparse(link)
                filename = ''.join([parsed_url.netloc, parsed_url.path])
                filename = filename.replace('/', '-')
                filename = filename.replace('_', '-')
                filename = filename.replace(':', '-')

                response = self.fetcher.fetch(link, to_file=os.path.join(path, filename))
                response.pop(u'content')
                url = response.pop(u'url')
                if url is not self.resources:
                    self.resources[url] = response


    def save_metadata(self):
        ''' save metadata
        '''
        if not self.path or not os.path.exists(self.path):
            raise RuntimeError('Error! The path for storing content is not defined')

        # save content metadata
        with io.open(os.path.join(self.path, 'index.json'), 'w', encoding='utf8') as meta:
            meta.write(unicode(json.dumps(self.metadata, indent=4, sort_keys=True)) + '\n')

        # save resources metadata
        with io.open(os.path.join(self.path, 'resources.json'), 'w', encoding='utf8') as meta:
            meta.write(unicode(json.dumps(self.resources, indent=4, sort_keys=True)) + '\n')

