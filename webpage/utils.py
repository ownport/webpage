import string
import urlparse

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


