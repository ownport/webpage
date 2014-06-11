import unittest

from webpage.cache import Cache


class CacheTest(unittest.TestCase):

    def test_new(self):
        ''' test_new
        '''
        cache = Cache(path='tests/data/test_cached_page/cache/')
        self.assertTrue(isinstance(cache, Cache))


    def test_failed_new(self):
        ''' test_failed_new
        '''
        self.assertRaises(RuntimeError, Cache, path='')
        self.assertRaises(RuntimeError, Cache, path='tests/data/test_cached_page/index.html')


    def test_get(self):
        ''' test_get
        '''
        url = 'http://localhost:8888/test_page/index.html'
        url_hash = '548d2ae1b77edbd86dd4f929d54d921e7db94637'

        cache = Cache(path='tests/data/test_cached_page/cache/')
        metadata, content = cache.get(url)
        self.assertEqual(metadata['url-hash'], url_hash)


    def test_get_not_in_cache(self):
        ''' test_get_not_in_cache
        '''
        cache = Cache(path='tests/data/test_cached_page/cache/')
        self.assertEqual(cache.get('http://localhost:8888/test_page/source.html'), (None, None))


    def test_put(self):
        ''' test_put
        '''
        headers = { 'url': 'http://localhost:8888/test_page/index.html' }
        content = '<html></html>'
        cache = Cache(path='tests/results/test_cached_page/cache/', create_dirs=True)
        cache.put(headers, content)
        self.assertEqual(cache.get('http://localhost:8888/test_page/index.html'), (headers, content))
