# -*- coding: utf-8 -*-
import io
import os
import json

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
                metadata = json.load(open(filepath, 'r'), encoding='utf-8')
                if metadata.get('url') != url:
                    continue
                content_filename = utils.offline_link(url, path=self.path)
                return metadata, self._get_content(content_filename)
        return None, None


    def put(self, headers, content):
        ''' put headers and content into cache
        '''
        filename = utils.offline_link(headers['url'], path=self.path)

        # save metadata
        with io.open('%s.metadata' % filename, 'w', encoding='utf8') as meta:
            meta.write(unicode(json.dumps(headers, indent=4, sort_keys=True)) + '\n')

        # save content
        with io.open(filename, 'w', encoding='utf8') as meta:
            meta.write(unicode(content))

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
        cached_file = open(filename, 'r')
        content = cached_file.read()
        return content




