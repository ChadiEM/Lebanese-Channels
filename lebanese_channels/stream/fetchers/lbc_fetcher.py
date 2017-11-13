import xml.etree.ElementTree as ET
from urllib.error import HTTPError

from lebanese_channels import utils
from lebanese_channels.stream.stream_fetcher import StreamFetcher, StreamError


class LBCStreamFetcher(StreamFetcher):
    def get_route_name(self) -> str:
        return 'lbc'

    def fetch_stream_url(self) -> str:
        try:
            html = utils.get_response('http://mobilefeeds.lbcgroup.tv/getCategories.aspx')
        except HTTPError:
            raise StreamError('lbc')

        root = ET.fromstring(html)
        playlist = root.find('watchLive')
        if playlist is not None:
            return playlist.text

        raise StreamError('lbc')
