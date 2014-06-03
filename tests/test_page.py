import os
import json
import unittest

from webpage.page import Webpage
from webpage.content import PageContent

from webpage.fetcher import CODES_OK

SOURCE_URL= 'http://localhost:8888/test_page/index.html'


class WebpageTest(unittest.TestCase):

    def test_new(self):
        ''' test_new
        '''
        wp = Webpage(url=SOURCE_URL)
        self.assertTrue(isinstance(wp, Webpage))
        self.assertTrue(isinstance(wp.content, PageContent))
        self.assertTrue('page' in wp.metadata)
        self.assertEqual(wp.metadata['page']['status-code'], CODES_OK)


    def test_failed_new(self):
        ''' test_failed_new
        '''
        self.assertRaises(RuntimeError, Webpage, url='http://255.255.255.255')


    def test_new_with_template(self):
        ''' test_new
        '''
        wp = Webpage(url=SOURCE_URL, template='tests/templates/simple.template')
        self.assertTrue(isinstance(wp, Webpage))


    def test_fetch_resources(self):
        ''' test_fetch_resources
        '''
        wp = Webpage(url=SOURCE_URL, path='tests/results/test_fetch_resources/')
        wp.get_resources(pattern=r'\.jpg$')
        self.assertEqual(len(wp.metadata['resources']), 4)
        wp.save()

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
        self.assertRaises(RuntimeError, wp.get_resources) 


    def test_save_path_not_defined(self):
        ''' test_save_metadata_path_not_defined
        '''
        wp = Webpage(url=SOURCE_URL)
        self.assertRaises(RuntimeError, wp.save) 


