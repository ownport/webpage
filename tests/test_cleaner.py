import unittest

from webpage.page import Webpage
from webpage.parser import Parser
from webpage.cleaner import Cleaner

SOURCE_URL= 'http://localhost:8888/test_cleaner/index.html'
wp = Webpage(url=SOURCE_URL)
wp.fetch_page()
parser = Parser(SOURCE_URL, wp.content)
CONTENT = parser.extract_content('//html/head', join_by=' ')

class ParserTest(unittest.TestCase):

    def test_clean_html(self):
        ''' test_clean_html
        '''
        cleaner = Cleaner()
        cleaned_content = cleaner.clean_html(CONTENT)
        self.assertGreater(len(CONTENT), len(cleaned_content))
