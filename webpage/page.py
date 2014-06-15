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

from os.path import basename
from urlparse import urlparse

from logging import getLogger
log = getLogger(__name__)

import utils

from content import PageContent
from template import PageTemplate
from cleaner import CleanerProfile
from cache.adapter import CachingHTTPAdapter


USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US)'


class Webpage(object):
    ''' Simple Web page archiver
    '''
    def __init__(self, url=None, headers={}, path=None, template=None, rules={}, cached=False):
        ''' __init__

        url         - webpage url
        headers     - HTTP Headers
        path        - drectory where files will be stored
        template    - webpage template
        rules       - rules for data extraction 
        cache       - cache, webpage.cache
        '''
        self.url = url
        
        self.headers = {'user-agent': USER_AGENT}
        if headers:
            self.headers.update(headers)

        self.metadata = {u'headers': {}, u'resources': {}}
        self.content = None

        self.path = path

        caching_adapter = None
        if cached and self.path:
            cache_dir = os.path.join(self.path, 'cache/')
            caching_adapter = CachingHTTPAdapter(path=cache_dir)
        self.fetcher = fetcher.Fetcher(headers=self.headers, caching_adapter=caching_adapter)

        self.template = None
        if template:
            self.template = PageTemplate(template)

        self.rules = rules

        self._retrieve_page()


    def _retrieve_page(self):
        ''' get page from cache if available
        '''
        response = self.fetcher.fetch(self.url)

        if response.get(u'status-code') == fetcher.CODES_OK: 
            self.content = PageContent(self.url, response.pop('content'))
            self.metadata['headers'] = response 
        
        else:
            raise RuntimeError('Error! Web page is not available, status-code: %s, %s' % 
                                (response.get('status-code'), self.url))


    def extract(self, xpath):
        ''' returns content extracted by xpath
        '''
        return self.content.extract(xpath)


    def get_resources(self, pattern=None):
        ''' fetch resources (images, css, javascript, video, ...)
        '''
        if not pattern:
            raise RuntimeError('Error! The pattern is not defined')

        pattern = re.compile(pattern)

        for link in self.content.links():
            if pattern and pattern.search(link):

                offline_filename = os.path.join(self.path, utils.offline_link(link))
                utils.makedirs(offline_filename)

                response = fetcher.fetch(link, to_file=offline_filename)
                response.pop(u'content')
                url = response.pop(u'url')
                if url is not self.metadata['resources']:
                    self.metadata['resources'][url] = response
                    response['filename'] = response['filename'].replace(self.path, '')
                    self.metadata['resources'][url]['filename'] = response['filename']


    def remove(self, xpath=None):
        ''' remove content by xpath
        '''
        self.content.remove(xpath)


    def clean(self, cleaner_profile):
        ''' clean content by cleaner profile
        '''
        if not isinstance(cleaner_profile, CleanerProfile):
            raise RuntimeError('Error! Incorrect cleaner type, %s' % type(cleaner_profile))
        cleaner_profile(self.content.content)


    def save(self, filename='index', metadata=True, resources=True):
        ''' save metadata and content

        filename - defines just filename for three files: 
            - <filename>.html 
            - <filename>.metadata 
            - <filename>.resources

        Only the first one is HTML file, the rest of files are JSON files

        metadata - if True, HTTP response information will be stored into .metadata file
        resources - If True, resources metadata will be stores into .resources file 
        '''
        if not self.path:
            raise RuntimeError('Error! The path for storing content is not defined')

        if not os.path.exists(self.path):
            utils.makedirs(self.path)

        # save content metadata
        if metadata:
            with io.open(os.path.join(self.path, '%s.metadata' % filename), 'w', encoding='utf8') as meta:
                meta.write(unicode(json.dumps(self.metadata['headers'], indent=4, sort_keys=True)) + '\n')

        # save resources metadata
        if resources and self.metadata['resources']:
            with io.open(os.path.join(self.path, '%s.resources' % filename), 'w', encoding='utf8') as meta:
                meta.write(unicode(json.dumps(self.metadata['resources'], indent=4, sort_keys=True)) + '\n')

        # save content
        offline_content = copy.deepcopy(self.content)
        offline_links = dict([(url, self.metadata['resources'][url]['filename']) for url in self.metadata['resources']])
        offline_content.make_links_offline(offline_links=offline_links)
        offline_content.save(os.path.join(self.path, '%s.html' % filename))

