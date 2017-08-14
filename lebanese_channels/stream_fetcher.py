import abc
import xml.etree.ElementTree
from typing import List

from lebanese_channels import utils


class StreamFetcher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_route_name(self) -> str:
        return ''

    @abc.abstractmethod
    def fetch_stream_data(self) -> List[str]:
        return []


class LBCStreamFetcher(StreamFetcher):
    def get_route_name(self) -> str:
        return 'lbc'

    def fetch_stream_data(self) -> List[str]:
        html = utils.get_html_response_for('http://mobilefeeds.lbcgroup.tv/getCategories.aspx')

        root = xml.etree.ElementTree.fromstring(html)
        playlist = root.find('watchLive').text

        html = utils.get_html_response_for(playlist)
        return make_response(playlist, html)


class GenericStreamFetcher(StreamFetcher):
    def __init__(self, route_name, url):
        self.route_name = route_name
        self.url = url

    def get_route_name(self) -> str:
        return self.route_name

    def fetch_stream_data(self) -> List[str]:
        html = utils.get_html_response_for(self.url)

        playlist = ''
        for line in html.splitlines():
            if 'file' in line and 'm3u8' in line:
                line_splitted = line.split('"')
                playlist = line_splitted[1]

        html = utils.get_html_response_for(playlist)
        return make_response(playlist, html)


def make_response(playlist: str, html: str) -> List[str]:
    list_response = []
    start_index = playlist.find('.m3u8')
    if start_index != -1:
        while playlist[start_index] != '/' and start_index > 0:
            start_index -= 1

    prefix = playlist[:start_index + 1]

    for line in html.splitlines():
        if not line.startswith('#'):
            list_response.append(prefix + line)
        else:
            list_response.append(line)

    return list_response
