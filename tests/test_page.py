import os
import json
import unittest

from webpage.page import Webpage
from webpage.content import PageContent
from webpage.cleaner import CleanerProfile

from webpage.fetcher import CODES_OK

SOURCE_URL= 'http://localhost:8888/test_page/index.html'
SOURCE_URL_CACHED= 'http://localhost:8888/index.html'


class WebpageTest(unittest.TestCase):

    def test_new(self):
        ''' test_new
        '''
        wp = Webpage(url=SOURCE_URL)
        self.assertTrue(isinstance(wp, Webpage))
        self.assertTrue(isinstance(wp.content, PageContent))
        self.assertTrue('headers' in wp.metadata)
        self.assertEqual(wp.metadata['headers']['status-code'], CODES_OK)


    def test_failed_new(self):
        ''' test_failed_new
        '''
        self.assertRaises(RuntimeError, Webpage, url='http://255.255.255.255')


    def test_fetch_page_with_user_agent(self):
        ''' test_fetch_page_with_user_agent
        '''
        wp = Webpage(url=SOURCE_URL, headers={'user-agent': 'ownport/webpage'})
        self.assertTrue(isinstance(wp, Webpage))


    def test_new_cached_page(self):
        ''' test_new_cached_page
        '''
        wp = Webpage(url=SOURCE_URL, path='tests/results/test_new_cached_page/', 
                    cached=True)
        self.assertTrue(isinstance(wp, Webpage))
        self.assertTrue(os.path.exists('tests/results/test_new_cached_page/'))


    def test_cached_page(self):
        ''' test_cached_page
        '''
        wp = Webpage(url=SOURCE_URL_CACHED, path='tests/results/test_cached_page/', cached=True)
        wp = Webpage(url=SOURCE_URL_CACHED, path='tests/results/test_cached_page/', cached=True)
        self.assertTrue(isinstance(wp, Webpage))
        self.assertEqual(wp.metadata['headers']['status-code'], 304)


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

        self.assertTrue(os.path.exists(os.path.join('tests/results/test_fetch_resources/', 'index.metadata')))
        self.assertTrue(os.path.exists(os.path.join('tests/results/test_fetch_resources/', 'index.resources')))

        index_json = json.loads(open(os.path.join('tests/results/test_fetch_resources/', 'index.metadata')).read())
        self.assertEqual(index_json['url'], SOURCE_URL)

        resources_json = json.loads(open(os.path.join('tests/results/test_fetch_resources/', 'index.resources')).read())
        self.assertTrue(u'http://localhost:8888/test_page/cover/001.jpg' in resources_json.keys())


    def test_fetch_resources_wo_pattern(self):
        ''' test_fetch_resources_wo_pattern
        '''
        wp = Webpage(url=SOURCE_URL)
        self.assertRaises(RuntimeError, wp.get_resources) 


    def test_extract(self):
        ''' test_extract
        '''
        wp = Webpage(url=SOURCE_URL)
        title = ''.join([title.content.text for title in wp.extract('//head/title/text()')])
        self.assertEqual(title, 'test-page-title') 


    def test_remove_content(self):
        ''' test_remove_content
        '''
        wp = Webpage(url=SOURCE_URL)
        self.assertRaises(RuntimeError, wp.remove)

        wp.remove('//a')
        wp.remove('//img')
        wp.remove('//link')
        wp.remove('//script')
        wp.get_resources('//a')
        wp.get_resources('//img')
        wp.get_resources('//link')
        wp.get_resources('//script')
        self.assertEqual(len(wp.metadata['resources']), 0) 

        self.assertRaises(RuntimeError, wp.remove, ' ')


    def test_clean_page(self):
        '''  test_clean_page
        '''
        class TestCleanerProfile(CleanerProfile):
            scripts = True
        test_cleaner_profile = TestCleanerProfile()

        wp = Webpage(url=SOURCE_URL)
        wp.clean(test_cleaner_profile)
        wp.get_resources('//script')
        self.assertEqual(wp.metadata['resources'], {})

        self.assertRaises(RuntimeError, wp.clean, TestCleanerProfile)


    def test_save_page(self):
        ''' test_save_page
        '''
        wp = Webpage(url=SOURCE_URL)
        self.assertRaises(RuntimeError, wp.save)

        wp = Webpage(url=SOURCE_URL, path='tests/results/test_page_save/')
        wp.save()
        self.assertTrue(os.path.exists(os.path.join('tests/results/test_page_save/', 'index.html')))
        self.assertTrue(os.path.exists(os.path.join('tests/results/test_page_save/', 'index.metadata')))


    def test_save_path_not_defined(self):
        ''' test_save_metadata_path_not_defined
        '''
        wp = Webpage(url=SOURCE_URL)
        self.assertRaises(RuntimeError, wp.save) 



