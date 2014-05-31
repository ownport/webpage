import os
import string


class PageTemplate(object):
    ''' PageTemplate
    '''
    def __init__(self, template, ):
        ''' __init__

        template - template filename
        '''
        if not os.path.exists(template):
            raise RuntimeError('Error! Template file not found, %s' % template)

        self.template = string.Template(open(template, 'r').read())


    def render(self, **kwargs):
        ''' template rendering
        '''
        return self.template.substitute(**kwargs)
        



