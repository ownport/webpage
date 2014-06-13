# -*- coding: utf- -*-

import unittest

from webpage.cache import Cache


class CacheTest(unittest.TestCase):

    def test_new(self):
        ''' test_new
        '''
        cache = Cache(path='tests/data/test_cache/')
        self.assertTrue(isinstance(cache, Cache))


    def test_failed_new(self):
        ''' test_failed_new
        '''
        self.assertRaises(RuntimeError, Cache, path='')
        self.assertRaises(RuntimeError, Cache, path='tests/data/test_cache/index.html')


    def test_get_not_in_cache(self):
        ''' test_get_not_in_cache
        '''
        cache = Cache(path='tests/data/test_cache/')
        self.assertEqual(cache.get('http://localhost:8888/test_page/source.html'), (None, None))


    def test_put(self):
        ''' test_put
        '''
        headers = { 'url': 'http://localhost:8888/test_page/index.html' }
        content = '<html></html>'
        cache = Cache(path='tests/results/test_cache/', create_dirs=True)
        cache.put(headers, content)
        self.assertEqual(cache.get('http://localhost:8888/test_page/index.html'), (headers, content))


    def test_conditional_headers(self):
        ''' test_conditional_headers
        '''
        self.assertEqual(Cache.conditional_headers({}), {})
        self.assertEqual(Cache.conditional_headers({'url': 'http://localhost:8888/'}), {})
        self.assertEqual(Cache.conditional_headers({'etag': '12345'}), {'if-none-match': '12345'})
        self.assertEqual(Cache.conditional_headers({'last-modified': '12/3/45'}), {'if-modified-since': '12/3/45'})


    def test_put_unicode_page(self):
        ''' test_put_unicode_page
        '''
        headers = { 'url': 'http://localhost:8888/test_page/index.html' }
        content = u'<html><body>контент, 内容, コンテンツ</body></html>'
        cache = Cache(path='tests/results/test_cache_unicode/', create_dirs=True)
        cache.put(headers, content)
        self.assertEqual(cache.get('http://localhost:8888/test_page/index.html'), 
                        (headers, content))




