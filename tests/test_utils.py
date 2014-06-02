import os
import json
import unittest

from webpage.utils import validate_url
from webpage.utils import offline_link


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
        self.assertEqual(offline_link('http://example.com?page=1', path='files/'), 'files/example.com-page=1')
        self.assertEqual(offline_link('http://example.com/index.html', path='files/'), 'files/example.com-index.html')

