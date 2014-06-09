import os
import unittest

from webpage import fetcher 
from webpage.fetcher import CODES_OK


SOURCE_URL= 'http://localhost:8888/test_page/index.html'


class FetcherTest(unittest.TestCase):

    def test_new(self):
        ''' test_new
        '''
        headers = {
            'user-agent': fetcher.USER_AGENT,
        }
        fetch = fetcher.Fetcher(headers=headers)

        response = fetch.fetch('http://localhost:8888/sitemap/sitemap.xml.gz', check=True)
        self.assertEqual(response['status-code'], CODES_OK)

        response = fetch.fetch('http://localhost:8888/sitemap/sitemap.xml.gz')
        content = response['content']
        self.assertTrue(content.startswith('<?xml version="1.0" encoding="UTF-8"?>'))


    def test_gzip_support(self):
        ''' test_gzip_support
        '''
        fetch = fetcher.Fetcher()
        response = fetch.fetch('http://localhost:8888/sitemap/sitemap.gz')
        content = response['content']
        self.assertTrue(content.startswith('<?xml version="1.0" encoding="UTF-8"?>'))


    def test_timeout(self):
        ''' test_timeout
        '''
        fetch = fetcher.Fetcher(timeout=1.)
        response = fetch.fetch('http://localhost:8888/timeout')
        self.assertEqual(response[u'status-code'], -2)


    def test_save_to_file(self):
        ''' test_save_to_file
        '''
        fetch = fetcher.Fetcher()
        response = fetch.fetch('http://localhost:8888/index.html', to_file='tests/results/index.html')
        self.assertEqual(response[u'status-code'], 200)


    def test_fetch_with_western_encoding(self):
        ''' test_save_to_file
        '''
        fetch = fetcher.Fetcher()
        response = fetch.fetch('http://localhost:8888/index-western-encoding.html')
        self.assertEqual(response[u'status-code'], 200)
        self.assertEqual(response[u'encoding'], u'utf-8')


    def test_fetch_file_with_orig_name(self):
        ''' test_fetch_file_with_orig_name
        '''
        fetch = fetcher.Fetcher()
        response = fetch.fetch('http://localhost:8888/text-file.txt', to_file='tests/results/textfile')
        self.assertEqual(response[u'status-code'], 200)
        self.assertFalse(os.path.exists('tests/results/textfile'))
        self.assertTrue(os.path.exists('tests/results/text-file.txt'))

