import abc
import xml.etree.ElementTree
from typing import List

import utils


class StreamFetcher(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def get_route_name() -> str:
        return

    @staticmethod
    @abc.abstractmethod
    def fetch_stream_url() -> List[str]:
        return


class LBCStreamFetcher(StreamFetcher):
    @staticmethod
    def get_route_name() -> str:
        return 'lbc'

    @staticmethod
    def fetch_stream_url() -> str:
        html = utils.get_html_response_for('http://mobilefeeds.lbcgroup.tv/getCategories.aspx')

        root = xml.etree.ElementTree.fromstring(html)
        playlist = root.find('watchLive').text

        return playlist


class JadeedStreamFetcher(StreamFetcher):
    @staticmethod
    def get_route_name() -> str:
        return 'jadeed'

    @staticmethod
    def fetch_stream_url() -> str:
        html = utils.get_html_response_for('http://player.l1vetv.com/aljadeed/index-1.php')

        playlist = ''
        for line in html.splitlines():
            if 'file' in line and 'm3u8' in line:
                line_splitted = line.split('"')
                playlist = line_splitted[1]

        return playlist


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
