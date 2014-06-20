import os
import string
import struct
import urlparse
import datetime

from gzip import GzipFile
from cStringIO import StringIO


RFC_1123_DT_STR = "%a, %d %b %Y %H:%M:%S GMT"
RFC_850_DT_STR = "%A, %d-%b-%y %H:%M:%S GMT"


def build_date_header(dt):
    ''' Given a Python datetime object, build a Date header value according to
    RFC 2616.

    RFC 2616 specifies that the RFC 1123 form is to be preferred, so that is
    what we use.
    '''
    return dt.strftime(RFC_1123_DT_STR)


def parse_date_header(header):
    ''' Given a date header in the form specified by RFC 2616, return a Python
    datetime object.

    RFC 2616 specifies three possible formats for date/time headers, and
    makes it clear that all dates/times should be in UTC/GMT. That is assumed
    by this library, which simply does everything in UTC. This currently does
    not parse the C asctime() string, because that's effort.

    This function does _not_ follow Postel's Law. If a format does not strictly
    match the defined strings, this function returns None. This is considered
    'safe' behaviour.
    '''
    try:
        dt = datetime.datetime.strptime(header, RFC_1123_DT_STR)
    except ValueError:
        try:
            dt = datetime.datetime.strptime(header, RFC_850_DT_STR)
        except ValueError:
            dt = None
    except TypeError:
        dt = None

    return dt


def date_header_or_default(header_name, default, response):

    value = response.headers.get(header_name, default)
    if isinstance(value, str):
        value = parse_date_header(value)
    
    return value


def expires_from_cache_control(header, current_time):
    ''' Given a Cache-Control header, builds a Python datetime object corresponding
    to the expiry time (in UTC). This function should respect all relevant
    Cache-Control directives.

    Takes current_time as an argument to ensure that 'max-age=0' generates the
    correct behaviour without being special-cased.

    Returns None to indicate that a request must not be cached.
    '''
    # Cache control header values are made of multiple comma separated fields.
    # Splitting them like this is probably a bad idea, but I'm going to roll with
    # it for now. We'll come back to it.
    fields = header.split(', ')
    duration = None

    for field in fields:
        # Right now we don't handle no-cache applied to specific fields. To be
        # as 'nice' as possible, treat any no-cache as applying to the whole
        # request. Bail early, because there's no reason to stick around.
        if field.startswith('no-cache') or field == 'no-store':
            return None

        if field.startswith('max-age'):
            _, duration = field.split('=')
            duration = int(duration)

    interval = timedelta(seconds=int(duration))

    return current_time + interval


def url_contains_query(url):
    ''' A very stupid function for determining if a URL contains a query string
    or not.
    '''
    if urlparse.urlparse(url).query:
        return True
    else:
        return False


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
    link = link.replace('&amp;', '-')
    link = link.replace('&', '-')
    link = link.replace('=', '-')
    link = os.path.join(path, link)
    return link


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


def makedirs(path):
    ''' create dirs if not exists
    '''
    dirname = os.path.dirname(path)
    if not dirname.endswith(os.sep):
        dirname += os.sep
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname


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


