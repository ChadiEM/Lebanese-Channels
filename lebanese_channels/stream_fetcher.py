import abc
import xml.etree.ElementTree

from lebanese_channels import utils


class StreamFetcher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_route_name(self) -> str:
        return ''

    @abc.abstractmethod
    def fetch_stream_url(self) -> str:
        return ''


class LBCStreamFetcher(StreamFetcher):
    def get_route_name(self) -> str:
        return 'lbc'

    def fetch_stream_url(self) -> str:
        html = utils.get_html_response_for('http://mobilefeeds.lbcgroup.tv/getCategories.aspx')

        root = xml.etree.ElementTree.fromstring(html)
        playlist = root.find('watchLive').text

        return playlist


class GenericStreamFetcher(StreamFetcher):
    def __init__(self, route_name, url):
        self.route_name = route_name
        self.url = url

    def get_route_name(self) -> str:
        return self.route_name

    def fetch_stream_url(self) -> str:
        html = utils.get_html_response_for(self.url)

        playlist = ''
        for line in html.splitlines():
            if 'file' in line and 'm3u8' in line:
                line_splitted = line.split('"')
                playlist = line_splitted[1]

        return playlist
