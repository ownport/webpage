import os
import json
import unittest

from webpage.page import Webpage
from webpage.fetcher import CODES_OK

SOURCE_URL= 'http://localhost:8888/test_page/index.html'


class WebpageTest(unittest.TestCase):

    def test_new(self):
        ''' test_new
        '''
        wp = Webpage(url=SOURCE_URL)
        self.assertTrue(isinstance(wp, Webpage))


    def test_new_with_template(self):
        ''' test_new
        '''
        wp = Webpage(url=SOURCE_URL, template='tests/templates/simple.template')
        self.assertTrue(isinstance(wp, Webpage))


    def test_page_is_available(self):
        ''' test_page_is_available
        '''
        wp = Webpage(url=SOURCE_URL)
        self.assertTrue(wp.is_available())

    def test_fetch_page(self):
        ''' test_fetch_page
        '''
        wp = Webpage(url=SOURCE_URL)
        wp.fetch_page()
        self.assertGreater(len(wp.content), 0)
        self.assertEqual(wp.metadata['status-code'], CODES_OK)

    def test_fetch_unavailable_page(self):
        ''' test_fetch_unavailable_page
        '''
        wp = Webpage(url='http://255.255.255.255')
        self.assertRaises(RuntimeError, wp.fetch_page)
        self.assertFalse(wp.is_available())
 

    def test_fetch_resources(self):
        ''' test_fetch_resources
        '''
        wp = Webpage(url=SOURCE_URL, path='tests/results/test_fetch_resources/')
        wp.fetch_resources(pattern=r'\.jpg$')
        self.assertEqual(len(wp.resources), 4)
        wp.save_metadata()

        self.assertTrue(os.path.exists(os.path.join('tests/results/test_fetch_resources/', 'index.json')))
        self.assertTrue(os.path.exists(os.path.join('tests/results/test_fetch_resources/', 'resources.json')))

        index_json = json.loads(open(os.path.join('tests/results/test_fetch_resources/', 'index.json')).read())
        self.assertEqual(index_json['url'], SOURCE_URL)

        resources_json = json.loads(open(os.path.join('tests/results/test_fetch_resources/', 'resources.json')).read())
        self.assertTrue(u'http://localhost:8888/test_page/cover/001.jpg' in resources_json.keys())


    def test_fetch_resources_wo_pattern(self):
        ''' test_fetch_resources_wo_pattern
        '''
        wp = Webpage(url=SOURCE_URL)
        self.assertRaises(RuntimeError, wp.fetch_resources) 


    def test_save_metadata_path_not_defined(self):
        ''' test_save_metadata_path_not_defined
        '''
        wp = Webpage(url=SOURCE_URL)
        self.assertRaises(RuntimeError, wp.save_metadata) 
