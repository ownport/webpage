import os
import unittest


from webpage.models import Request, Response 


class ModelsTest(unittest.TestCase):

    def test_new_request(self):
        ''' test_new_request
        '''
        r = Request()
        self.assertTrue(isinstance(r, Request))


    def test_new_response(self):
        ''' test_new_response
        '''
        r = Response()
        self.assertTrue(isinstance(r, Response))


