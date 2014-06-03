from lxml.html import defs
from lxml.html.clean import Cleaner


class CleanerProfile(Cleaner):
    ''' Webpage cleaner profile

    remove the all or partially suspicious content from this
    unparsed document. It supports removing embedded or script
    content, special tags, CSS style annotations and much more.
    '''
    scripts = True
    javascript = True
    comments = True
    style = True
    links = False
    meta = False
    page_structure = False
    processing_instructions = False
    embedded = False
    frames = False
    forms = False
    annoying_tags = False
    remove_tags = None
    allow_tags = None
    kill_tags = None
    remove_unknown_tags = False
    safe_attrs_only = False
    safe_attrs = defs.safe_attrs
    add_nofollow = False
    host_whitelist = ()
    whitelist_tags = set()
