import mock
import requests
import unittest

from webpage.cache import URLRulesHTTPCache


URL_RULES = [
    'http://example.com',
    'http://example.com/pages/\d+/',
]


class URLRulesHTTPCacheTest(unittest.TestCase):
    
    def test_new(self):
        ''' test_new
        '''
        urls = [
            'http://example.com/',
            'http://example.com/pages/\d+/',
        ]

        self.assertRaises(RuntimeError, URLRulesHTTPCache, 'urls')
        self.assertRaises(RuntimeError, URLRulesHTTPCache, urls='urls')

        self.assertTrue(isinstance(URLRulesHTTPCache(urls, path='tests/results/test_cache/'), 
                        URLRulesHTTPCache))


    @mock.patch('webpage.utils.save')
    def test_response_store(self, mock_utils_save):
        ''' test_response_store
        '''
        cache = URLRulesHTTPCache(URL_RULES, path='tests/results/test_cache/')
        resp = mock.Mock(    spec=requests.Response, url='http://example.com', 
                            headers={}, encoding='utf-8', status_code=200,
                            content='mock-save-content')
        cache.store(resp)
        self.assertTrue(mock_utils_save.called)


    def test_request_store_not_in_the_list(self):
        ''' test_request_store_not_in_the_list
        '''
        cache = URLRulesHTTPCache(URL_RULES, path='tests/results/test_cache/')
        resp = mock.Mock(spec=requests.Response, url='http://foo.com')
        result = cache.store(resp)
        self.assertFalse(result)


    def test_request_retrieve_not_in_the_list(self):
        ''' test_request_retrieve_not_in_the_list
        '''
        cache = URLRulesHTTPCache(URL_RULES, path='tests/results/test_cache/')
        req = mock.Mock(spec=requests.Request, url='http://foo.com')
        resp = cache.retrieve(req)
        self.assertIsNone(resp)


    @mock.patch('webpage.utils.read')
    def test_request_retrieve(self, mock_utils_read):
        ''' test_request_retrieve
        '''
        mock_utils_read.side_effect=[
            '{"status-code":200, "url": "http://example.com"}', 
            u'mock-read-content',
        ]
        cache = URLRulesHTTPCache(URL_RULES, path='tests/results/test_cache/')
        req = mock.Mock(    spec=requests.Response, url='http://example.com', 
                            headers={}, encoding='utf-8', status_code=200,
                            content=u'mock-read-content')
        resp = cache.retrieve(req)
        self.assertTrue(mock_utils_read.called)
        self.assertIsNotNone(resp)
        self.assertTrue(isinstance(resp, requests.Response))

