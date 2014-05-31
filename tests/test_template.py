# -*- coding: utf-8 -*-

import unittest

from webpage.template import PageTemplate

class PageTemplateTest(unittest.TestCase):

    def test_error_handling(self):
        ''' test_error_handling
        '''
        self.assertRaises(RuntimeError, PageTemplate, 'unknown.template')


    def test_title_template(self):
        ''' test_title_template
        '''
        template = PageTemplate('tests/templates/title.template')
        self.assertEqual(template.render(title='Test title').strip(), '<h1>Test title</h1>')


    def test_title_template(self):
        ''' test_title_template
        '''
        template = PageTemplate('tests/templates/simple.template')
        self.assertEqual(template.render(title='Test', body='Test').strip(), 
                        '<html>\n<head>\n\t<title>Test</title>\n</head>\n<body>\n\tTest\n</body>\n</html>')


