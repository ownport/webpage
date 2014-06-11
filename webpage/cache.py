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

        if not os.path.isdir(path):
            raise RuntimeError('Error! Path is not directory, %s' % path)
            

    def get(self, url):
        ''' get metadata by url
        '''
        for f in os.listdir(self.path):
            filepath = os.path.join(self.path, f)
            if os.path.isfile(filepath) and f.endswith('.metadata'):
                metadata = json.load(open(filepath, 'r'), encoding='utf-8')
                if metadata.get('url') != url:
                    continue
                content_filename = os.path.join(self.path, utils.offline_link(url, path=''))
                return metadata, open(content_filename).read()
        return None, None


    def put(self, headers, content):
        ''' put headers and content into cache
        '''
        filename = utils.offline_link(headers['url'], path='')
        # save content metadata
        with io.open(os.path.join(self.path, '%s.metadata' % filename), 'w', encoding='utf8') as meta:
            meta.write(unicode(json.dumps(headers, indent=4, sort_keys=True)) + '\n')

        # save content
        with io.open(os.path.join(self.path, filename), 'w', encoding='utf8') as meta:
            meta.write(unicode(content))






