# -*- coding: utf-8 -*-

import unittest

from webpage.page import Webpage
from webpage.parser import Parser

SOURCE_URL='http://localhost:8888/test_parser/index.html'
wp = Webpage(url=SOURCE_URL)
wp.fetch_page()

class ParserTest(unittest.TestCase):

    def test_handling_errors(self):
        ''' test_handling_errors
        '''
        self.assertRaises(RuntimeError, Parser)
        self.assertRaises(RuntimeError, Parser, 'http://www.example.com')
        

    def test_extract_links(self):
        ''' test_extract_link
        '''
        parser = Parser(SOURCE_URL, wp.content)
        if SOURCE_URL in parser.extract_links():
            return
        raise RuntimeError("Source URL was not found in extracted links")


    def test_extract_content(self):
        ''' test_extract_content
        '''
        parser = Parser(SOURCE_URL, wp.content)
        self.assertGreater(len(parser.extract_content('//head/title/text()', join_by=' ')), 10) 
        self.assertEqual(parser.extract_content('//body/h1[@class="lang-ru"]/text()', join_by=' '), u'Тестовая страница')


    def test_failed_extract_content(self):
        ''' test_failed_extract_content
        '''
        parser = Parser(SOURCE_URL, wp.content)
        self.assertRaises(RuntimeError, parser.extract_content, '//head/title/text()', join_by=[1,2,3]) 


    def test_extract_content_with_links(self):
        ''' test_extract_content_with_links
        '''
        parser = Parser(SOURCE_URL, wp.content)
        block = parser.extract_content('//div[@class="item-info"]', join_by=' ')
        parser_block = Parser(SOURCE_URL, block)
        if SOURCE_URL in parser_block.extract_links():
            return
        raise RuntimeError("Source URL was not found in extracted links")


    def test_extract_content_by_rules(self):
        ''' test_extract_content_by_rules
        '''
        parser = Parser(SOURCE_URL, wp.content)
        rules = {
            'title': '//html/head/title/text()',
            'meta': '//html/head/meta',
        }
        result = parser.extract_content_by_rules(rules)
        self.assertGreater(len(result['title']), 0)
        self.assertGreater(len(result['meta']), 0)

