# -*- coding: utf-8 -*-

import lxml
import urlparse

from utils import validate_url
from utils import offline_link

from lxml.html import HtmlElement


class PageContent(object):
    ''' Page Content
    '''
    def __init__(self, base_url=None, content=None):
        ''' __init__

        content     - HTML content (string or unicode)
        '''
        if content is None or not isinstance(content, (str, unicode, HtmlElement)):
            raise RuntimeError('Error! Incorrect content type, %s' % type(content))
        
        if isinstance(content, (str, unicode)):
            try:
                self.content = lxml.html.fromstring(content)
            except lxml.etree.ParserError, err:
                raise RuntimeError('Error! HTML parsing failed: %s' % err)
        else:
            self.content = content

        if not all([base_url, validate_url(base_url)]):
            raise RuntimeError('Error! Incorrect base_url, %s' % base_url)
        self.base_url = base_url
        self.make_links_absolute()


    def make_links_absolute(self):
        ''' makes all links in the document absolute, assuming that 
        base_href is the URL of the document.
        '''
        self.content.make_links_absolute(self.base_url)


    def make_links_offline(self):
        ''' Rename all the links in the document for offline use. 
        '''
        for element, attribute, link, pos in self.content.iterlinks():
            element.set(attribute, offline_link(link))


    def links(self):
        ''' extract links
        '''
        links = []
        for element, attribute, link, pos in self.content.iterlinks():
            if link not in links:
                links.append(link)
        return links


    def extract(self, xpath=None):
        ''' extract content by xpath
        '''
        elements = list()
        for element in self.content.xpath(xpath):
            if element is not None:
                elements.append(PageContent(self.base_url, element))
        return elements

    
    def to_unicode(self):
        ''' convert content to unicode 
        '''
        content = lxml.html.tostring(self.content, pretty_print=True, encoding='utf8') 
        return content.strip()


    def save(self, filename):
        ''' save content to file
        '''
        content = lxml.etree.ElementTree(self.content)
        content.write(filename, encoding='utf8', method="html")