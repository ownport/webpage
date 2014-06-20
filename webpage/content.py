# -*- coding: utf-8 -*-

import lxml
import urlparse

from cleaner import Cleaner
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


    def make_links_offline(self, offline_links={}):
        ''' Rename links in the document for offline use.

        if offline_links is not defined, rename all links 
        '''

        for element, attribute, link, pos in self.content.iterlinks():
            if offline_links:
                if link in offline_links:
                    for k,v in element.items():
                        if v.find(link) >= 0:
                            element.set(k, v.replace(link, offline_links[link]))
            else:
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


    def remove(self, xpath=None):
        ''' remove content by xpath
        '''
        if not xpath:
            raise RuntimeError('Error! Xpath is not defined')
        try:
            for element in self.content.xpath(xpath):
                element.getparent().remove(element)
        except lxml.etree.XPathEvalError:
            raise RuntimeError('Error! Incorrect Xpath definition, %s' % xpath)

    
    def to_unicode(self):
        ''' convert content to unicode 
        '''
        content = lxml.html.tostring(self.content)
        return unicode(content.strip())


    def save(self, filename):
        ''' save content to file
        '''
        content = lxml.etree.ElementTree(self.content)
        content.write(filename, encoding='utf-8', method="html")