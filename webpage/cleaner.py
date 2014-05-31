from lxml.html import defs
from lxml.html.clean import Cleaner as lxmlCleaner

''' remove the all or partially suspicious content from this 
unparsed document. It supports removing embedded or script 
content, special tags, CSS style annotations and much more.
'''

class Cleaner(lxmlCleaner):
    ''' Webpage cleaner
    '''
    scripts = True
    javascript = True
    comments = True
    style = False
    links = False
    meta = False
    page_structure = False
    processing_instructions = True
    embedded = True
    frames = True
    forms = True
    annoying_tags = True
    remove_tags = None
    allow_tags = None
    kill_tags = None
    remove_unknown_tags = True
    safe_attrs_only = False
    safe_attrs = defs.safe_attrs
    add_nofollow = False
    host_whitelist = ()
    whitelist_tags = set()

    def __init__(self, **kwargs):
        ''' __init__
        '''
        super(Cleaner, self).__init__(**kwargs)
