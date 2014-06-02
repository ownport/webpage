# -*- coding: utf-8 -*-
#
#   Simple web archive format
#

import io
import os
import re
import json
import copy
import fetcher 
import tempfile

from os.path import basename
from urlparse import urlparse

from utils import offline_link
from content import PageContent
from template import PageTemplate


USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US)'


class Webpage(object):
    ''' Simple Web page archiver
    '''
    def __init__(self, url=None, headers={}, path=None, template=None, rules={}):
        ''' __init__

        url         - webpage url
        headers     - HTTP Headers
        path        - drectory where files will be stored
        template    - webpage template
        rules       - rules for data extraction 
        '''
        self.url = url
        if not headers:
            self.headers = {'user-agent': USER_AGENT}

        self.metadata = {'page': {}, 'resources': {}}
        response = fetcher.fetch(url, headers)
        if response.get('status-code', None) == fetcher.CODES_OK: 
            self.content = PageContent(self.url, response.pop('content'))
            self.metadata['page'] = response 
        else:
            raise RuntimeError('Error! Web page is not available: %s' % self.url)

        self.path = path

        self.template = None
        if template:
            self.template = PageTemplate(template)

        self.rules = rules


    def _make_offline_dir(self, filename):
        ''' check if directory for offline file is exists and create it, if not
        '''
        dirname = os.path.dirname(filename) 
        if not os.path.exists(dirname):
            os.makedirs(dirname)


    def resources(self, pattern=None):
        ''' fetch resources (images, css, javascript, video, ...)
        '''
        if not pattern:
            raise RuntimeError('Error! The pattern is not defined')

        pattern = re.compile(pattern)

        for link in self.content.links():
            if pattern and pattern.search(link):

                offline_filename = os.path.join(self.path, offline_link(link))
                self._make_offline_dir(offline_filename)

                response = fetcher.fetch(link, to_file=offline_filename)
                response.pop(u'content')
                url = response.pop(u'url')
                if url is not self.metadata['resources']:
                    self.metadata['resources'][url] = response


    def save(self):
        ''' save metadata and content
        '''
        if not self.path:
            raise RuntimeError('Error! The path for storing content is not defined')

        test_fullpath = os.path.join(self.path, 'test.html')
        if not os.path.exists(test_fullpath):
            self._make_offline_dir(test_fullpath)

        # save content metadata
        with io.open(os.path.join(self.path, 'index.json'), 'w', encoding='utf8') as meta:
            meta.write(unicode(json.dumps(self.metadata['page'], indent=4, sort_keys=True)) + '\n')

        # save resources metadata
        if self.metadata['resources']:
            with io.open(os.path.join(self.path, 'resources.json'), 'w', encoding='utf8') as meta:
                meta.write(unicode(json.dumps(self.metadata['resources'], indent=4, sort_keys=True)) + '\n')

        # save content
        offline_content = copy.deepcopy(self.content)
        offline_content.make_links_offline()
        offline_content.save(os.path.join(self.path, 'source.html'))

