import mock
import unittest

from webpage.adapter import CachingHTTPAdapter


class CachingHTTPAdapterTest(unittest.TestCase):
    
    def test_new_failed(self):
        ''' test_new_failed
        '''
        self.assertRaises(RuntimeError, CachingHTTPAdapter)


    def test_new(self):
        ''' test_new
        '''
        self.assertTrue(isinstance(CachingHTTPAdapter(mock.Mock), CachingHTTPAdapter))

        
