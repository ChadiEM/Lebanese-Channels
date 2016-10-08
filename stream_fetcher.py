import abc
import xml.etree.ElementTree

import utils


class StreamFetcher(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def get_route_name():
        return

    @staticmethod
    @abc.abstractmethod
    def fetch_stream_data():
        return


class LBCStreamFetcher(StreamFetcher):
    @staticmethod
    def get_route_name():
        return 'lbc'

    @staticmethod
    def fetch_stream_data():
        html = utils.get_html_response_for('http://mobilefeeds.lbcgroup.tv/getCategories.aspx')

        root = xml.etree.ElementTree.fromstring(html)
        playlist = root.find('watchLive').text
        html = utils.get_html_response_for(playlist)

        return make_response(playlist, html)


class JadeedStreamFetcher(StreamFetcher):
    @staticmethod
    def get_route_name():
        return 'jadeed'

    @staticmethod
    def fetch_stream_data():
        html = utils.get_html_response_for('http://player.l1vetv.com/aljadeed/index-1.php')

        playlist = ''
        for line in html.splitlines():
            if 'file' in line and 'm3u8' in line:
                line_splitted = line.split('"')
                playlist = line_splitted[1]

        html = utils.get_html_response_for(playlist)

        return make_response(playlist, html)


def make_response(playlist, html):
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
