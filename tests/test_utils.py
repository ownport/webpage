import os
import json
import unittest

from webpage import utils
from datetime import datetime
from datetime import timedelta


class UtilsTest(unittest.TestCase):

    def test_validate_url(self):
        ''' test_validate_url
        '''
        self.assertTrue(utils.validate_url('http://example.com'))
        self.assertTrue(utils.validate_url('http://example.com/1'))
        self.assertTrue(utils.validate_url('http://example.com/?page=1'))
        self.assertTrue(utils.validate_url('http://example.com/run.cgi?page=1'))
        self.assertTrue(utils.validate_url('http://localhost:8888/test_page/index.html'))
        
        self.assertFalse(utils.validate_url('http://example,com'))
        self.assertFalse(utils.validate_url('htp://example.com'))
        self.assertFalse(utils.validate_url('://example.com'))
        self.assertFalse(utils.validate_url('//example.com'))
        self.assertFalse(utils.validate_url('example.com'))

    def test_offline_link(self):
        ''' test_offline_link
        '''
        self.assertEqual(utils.offline_link('http://example.com', path='files/'), 'files/example.com')
        self.assertEqual(utils.offline_link('http://example.com?page=1', path='files/'), 'files/example.com-page-1')
        self.assertEqual(utils.offline_link('http://example.com/index.html', path='files/'), 'files/example.com-index.html')
        self.assertEqual(utils.offline_link('http://example.com/index.html?ajax&amp;test', path='files/'), 
                        'files/example.com-index.html-ajax-test')


    def test_gunzip_no_gzip_file_raises(self):
        with open('tests/data/compressed/feed-sample1.xml', 'rb') as f:
            self.assertRaises(IOError, utils.gunzip, f.read())


    def test_gunzip_basic(self):
        with open('tests/data/compressed/feed-sample1.xml.gz', 'rb') as f:
            text = utils.gunzip(f.read())
            self.assertEqual(len(text), 9950)


    def test_gunzip_truncated(self):
        with open('tests/data/compressed/truncated-crc-error.gz', 'rb') as f:
            text = utils.gunzip(f.read())
            assert text.endswith('</html')


    def test_gunzip_truncated_short(self):
        with open('tests/data/compressed/truncated-crc-error-short.gz', 'rb') as f:
            text = utils.gunzip(f.read())
            assert text.endswith('</html>')


    def test_expires_from_cache_control(self):
        ''' test_expires_from_cache_control
        '''
        now = datetime.utcnow()
        cache_control_header = 'must-revalidate, post-check=0, pre-check=0'
        self.assertIsNone(utils.expires_from_cache_control(cache_control_header, now))

        cache_control_header = 'cache, max-age=100'
        self.assertEqual(utils.expires_from_cache_control(cache_control_header, now),
                        now+timedelta(seconds=100))
