import xml.etree.ElementTree as ET

from lebanese_channels import utils
from lebanese_channels.stream.stream_fetcher import StreamFetcher


class LBCStreamFetcher(StreamFetcher):
    def get_route_name(self) -> str:
        return 'lbc'

    def fetch_stream_url(self) -> str:
        html = utils.get_response('http://mobilefeeds.lbcgroup.tv/getCategories.aspx')

        root = ET.fromstring(html)
        playlist = root.find('watchLive').text

        return playlist
