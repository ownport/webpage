import os
import json
import unittest

from webpage.fetcher import gunzip
from webpage.utils import validate_url
from webpage.cache.utils import offline_link


class UtilsTest(unittest.TestCase):

    def test_validate_url(self):
        ''' test_validate_url
        '''
        self.assertTrue(validate_url('http://example.com'))
        self.assertTrue(validate_url('http://example.com/1'))
        self.assertTrue(validate_url('http://example.com/?page=1'))
        self.assertTrue(validate_url('http://example.com/run.cgi?page=1'))
        self.assertTrue(validate_url('http://localhost:8888/test_page/index.html'))
        
        self.assertFalse(validate_url('http://example,com'))
        self.assertFalse(validate_url('htp://example.com'))
        self.assertFalse(validate_url('://example.com'))
        self.assertFalse(validate_url('//example.com'))
        self.assertFalse(validate_url('example.com'))

    def test_offline_link(self):
        ''' test_offline_link
        '''
        self.assertEqual(offline_link('http://example.com', path='files/'), 'files/example.com')
        self.assertEqual(offline_link('http://example.com?page=1', path='files/'), 'files/example.com-page-1')
        self.assertEqual(offline_link('http://example.com/index.html', path='files/'), 'files/example.com-index.html')
        self.assertEqual(offline_link('http://example.com/index.html?ajax&amp;test', path='files/'), 
                        'files/example.com-index.html-ajax-test')


    def test_gunzip_no_gzip_file_raises(self):
        with open('tests/data/compressed/feed-sample1.xml', 'rb') as f:
            self.assertRaises(IOError, gunzip, f.read())


    def test_gunzip_basic(self):
        with open('tests/data/compressed/feed-sample1.xml.gz', 'rb') as f:
            text = gunzip(f.read())
            self.assertEqual(len(text), 9950)


    def test_gunzip_truncated(self):
        with open('tests/data/compressed/truncated-crc-error.gz', 'rb') as f:
            text = gunzip(f.read())
            assert text.endswith('</html')


    def test_gunzip_truncated_short(self):
        with open('tests/data/compressed/truncated-crc-error-short.gz', 'rb') as f:
            text = gunzip(f.read())
            assert text.endswith('</html>')

