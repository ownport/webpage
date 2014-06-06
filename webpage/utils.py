import string
import struct
import urlparse


from gzip import GzipFile
from cStringIO import StringIO


def validate_url(url):
    ''' simple URL validation

    return True if URL is correct
    '''
    parts = urlparse.urlparse(url)
    if not all([parts.scheme, parts.netloc]):
        return False
    if not set(parts.netloc) <= set(string.letters + string.digits + '-.:'):  # and others?
        return False
    if not parts.scheme in ['http', 'https', 'ftp']:
        return False
    return True


def offline_link(link, path='files/'):
    ''' rename link for offline use
    ''' 
    parsed_link = urlparse.urlparse(link)
    link = ''.join([parsed_link.netloc, parsed_link.path])
    for arg in [parsed_link.params, parsed_link.query, parsed_link.fragment]:
        if arg:
            link = '-'.join([link, arg])
    link = link.replace('/', '-')
    link = link.replace('_', '-')
    link = link.replace(':', '-')
    link = urlparse.urljoin(path, link)
    return link


def gunzip(data):
    """Gunzip the given data and return as much data as possible.

    This is resilient to CRC checksum errors.

    source: https://github.com/scrapy/scrapy/blob/master/scrapy/utils/gz.py
    """
    output = ''
    chunk = '.'
    with GzipFile(fileobj=StringIO(data)) as f: 
        while chunk:
            try:
                chunk = f.read(65536)
                output += chunk
            except (IOError, EOFError, struct.error), err:
                # complete only if there is some data, otherwise re-raise
                # see issue 87 (https://github.com/scrapy/scrapy/issues/87) 
                # about catching struct.error some pages are quite small so 
                # output is '' and f.extrabuf contains the whole page content
                if output or f.extrabuf:
                    output += f.extrabuf
                    break
                else:
                    raise
    return output


