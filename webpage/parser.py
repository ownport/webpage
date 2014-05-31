import re

from lxml import html
from lxml import etree

class Parser(object):
    ''' Parser
    '''
    def __init__(self, base_url=None, content=None, cleanup=True):
        ''' __init__
        '''
        if not base_url:
            raise RuntimeError('Error! The URL cannot be None')
        self.base_url = base_url

        if not content:
            raise RuntimeError('Error! The content cannot be None')
        self.content = content
        self.content = html.fromstring(self.content, base_url=self.base_url)

        # This makes all links in the document absolute, assuming that 
        # base_href is the URL of the document.
        self.content.make_links_absolute(self.base_url)


    def extract_content(self, xpath, join_by=None):
        ''' extract content by xpath

        join_by - join results by `join_by` character 
        '''
        results = [self.tostring(c).strip() for c in self.content.xpath(xpath)]
        if join_by or join_by == '':
            if isinstance(join_by, (str, unicode)):
                results = join_by.join(results)
            else:
                raise RuntimeError('Error! join_by must be str or unicode, %s' % type(join_by))
        return results


    def extract_content_by_rules(self, rules=dict()):
        ''' extract content by rules
        '''
        result = dict()
        for name, rule in rules.items():
            result[name] = self.extract_content(rule)
        return result


    def extract_links(self):
        ''' extract links
        '''
        links = []
        for link_info in self.content.iterlinks():
            element, attribute, link, pos = link_info 
            if link not in links:
                links.append(link)
            # yield {'tag': element.tag, 'attr': attribute, 'links': link, 'pos': pos }
        return links


    def tostring(self, obj):
        ''' convert to string 
        '''
        if isinstance(obj, (str, unicode)):
            return obj
        return etree.tostring(obj, pretty_print=True, encoding='utf8')