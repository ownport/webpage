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
from cleaner import CleanerProfile


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


    def get_resources(self, pattern=None):
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
                    self.metadata['resources'][url]['filename'] = offline_link(link)


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
            self._make_offline_dir(self.path)

        # save content metadata
        if metadata:
            with io.open(os.path.join(self.path, '%s.metadata' % filename), 'w', encoding='utf8') as meta:
                meta.write(unicode(json.dumps(self.metadata['page'], indent=4, sort_keys=True)) + '\n')

        # save resources metadata
        if resources and self.metadata['resources']:
            with io.open(os.path.join(self.path, '%s.resources' % filename), 'w', encoding='utf8') as meta:
                meta.write(unicode(json.dumps(self.metadata['resources'], indent=4, sort_keys=True)) + '\n')

        # save content
        offline_content = copy.deepcopy(self.content)
        offline_links = dict([(url, self.metadata['resources'][url]['filename']) for url in self.metadata['resources']])
        offline_content.make_links_offline(offline_links=offline_links)
        offline_content.save(os.path.join(self.path, '%s.html' % filename))

