import unittest

import test_core

from webpage.cleaner import Cleaner

class ParserTest(unittest.TestCase):

    def test_clean_html(self):
        ''' test_clean_html
        '''
        cleaner = Cleaner()
        cleaned_content = cleaner.clean_html(test_core.TEST_CONTENT)
        self.assertGreater(len(test_core.TEST_CONTENT), len(cleaned_content))

