# -*- coding: utf-8 -*-
import io
import os
import json
import codecs

import utils


class Cache(object):
    ''' local Webpage cache
    '''
    def __init__(self, path, create_dirs=False):
        ''' __init__

        path    - the path to local webpage cache
        '''
        if not os.path.exists(path) and not create_dirs:
            raise RuntimeError('Error! Path to cache does not exist, %s' % path)
        self.path = utils.makedirs(path)


    def get(self, url):
        ''' get metadata by url
        '''
        for f in os.listdir(self.path):
            filepath = os.path.join(self.path, f)
            if os.path.isfile(filepath) and f.endswith('.metadata'):
                metadata = json.loads(self._get_content(filepath))
                if metadata.get('url') != url:
                    continue
                content_filename = utils.offline_link(url, path=self.path)
                return metadata, self._get_content(content_filename)
        return None, None


    def put(self, headers, content):
        ''' put headers and content into cache
        '''
        filename = utils.offline_link(headers['url'], path=self.path)
        self._put_content('%s.metadata' % filename, 
                    json.dumps(headers, indent=4, sort_keys=True) + '\n')
        self._put_content(filename, content)


    @staticmethod
    def conditional_headers(headers={}):
        ''' select only 'ETag' and 'Last-Modified' keys and 
        transform its to 'If-None-Match' and 'If-Modified-Since'
        
        returns dict only with two keys: 'If-None-Match' and 'If-Modified-Since'
        ''' 
        new_headers = {}

        if 'etag' in headers:
            new_headers['if-none-match'] = headers['etag']

        if 'last-modified' in headers:
            new_headers['if-modified-since'] = headers['last-modified']

        return new_headers


    def _get_content(self, filename):
        ''' get content from cache_dir
        '''
        with codecs.open(filename, 'r', encoding='utf8') as cached_file:
            content = cached_file.read()
        return content


    def _put_content(self, filename, content):
        ''' put content to cache
        '''
        with codecs.open(filename, 'w', encoding='utf8') as cached_file:
            cached_file.write(content)



