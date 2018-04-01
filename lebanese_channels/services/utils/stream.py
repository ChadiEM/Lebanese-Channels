from urllib.error import HTTPError

from lebanese_channels.channel import StreamError
from lebanese_channels.services.utils.web import get_response


def fetch_from(url):
    try:
        html = get_response(url)
        for line in html.splitlines():
            if ('file' in line or 'Link' in line) and 'm3u8' in line:
                return line.split('"')[1]
    except HTTPError:
        raise StreamError(url)

    raise StreamError(url)
