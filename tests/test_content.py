import os
import unittest

import test_core

from webpage.content import PageContent


class PageContentTest(unittest.TestCase):

    def test_failed_new(self):
        ''' test_failed_new
        '''
        self.assertRaises(RuntimeError, PageContent, None, None)
        self.assertRaises(RuntimeError, PageContent, 'http://example.com', None)
        self.assertRaises(RuntimeError, PageContent, None, '</html>')
        self.assertRaises(RuntimeError, PageContent, 'http://example,com', test_core.TEST_CONTENT)


    def test_new(self):
        ''' test_new
        '''
        self.assertTrue(isinstance(
                                PageContent('http://example.com', test_core.TEST_CONTENT), 
                                PageContent))
        self.assertRaises(isinstance(
                                PageContent('http://example.com', '<html><a <a <a </html>'), 
                                PageContent))


    def test_extract_links(self):
        ''' test_extract_links
        '''
        content = PageContent('http://example.com', test_core.TEST_CONTENT)
        content.make_links_absolute()
        self.assertEqual(set(content.links()), set(test_core.TEST_URL_LIST)) 


    def test_offline(self):
        ''' test_offline
        '''
        content = PageContent('http://example.com', test_core.TEST_CONTENT)
        content.make_links_offline()
        self.assertEqual(set(content.links()), set(test_core.TEST_OFFLINE_URL_LIST)) 


    def test_extract_content(self):
        ''' test_extract_content
        '''
        content = PageContent('http://example.com', test_core.TEST_CONTENT)
        self.assertEqual(content.extract(xpath='//body/any'), [])
        self.assertEqual(len(content.extract(xpath='//body/a')), 2)
        self.assertEqual(len(content.extract(xpath='//body/img')), 1)


    def test_to_unicode(self):
        ''' test_to_unicode
        '''
        content = PageContent('http://example.com', test_core.TEST_CONTENT)
        self.assertEqual([c.to_unicode() for c in content.extract(xpath='//body/img')], 
                        ['<img src="http://localhost:8888/logo.jpg">'])

        self.assertEqual([c.to_unicode() for c in content.extract(xpath='//body/a')], 
                        ['<a href="http://example.com/index.html">Home</a>',
                        '<a href="http://example.com/articles.html">Articles</a>'])


