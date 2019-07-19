import urllib
import urllib.parse
import urllib.request
from urllib.error import HTTPError

from lebanese_channels.channel import StreamError, StreamNotFoundError


def fetch_from(url):
    try:
        html = get_response(url)
        for line in html.splitlines():
            if ('file' in line or 'Link' in line) and 'm3u8' in line:
                return line.split('"')[1]
    except HTTPError:
        raise StreamError(url)

    raise StreamNotFoundError(url)


def get_response(url: str, params=None):
    data = None if params is None else urllib.parse.urlencode(params).encode('utf-8')
    req = urllib.request.Request(url, data=data)

    req.add_header('User-Agent',
                   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0')

    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    response.close()
    return html
