from lebanese_channels.channel import Channel
from lebanese_channels.services.epg_parsers.jadeed_parser import JadeedParser
from lebanese_channels.services.utils import stream
from lebanese_channels.services.utils.epg import fetch_epg


class Jadeed(Channel):
    def get_name(self) -> str:
        return 'Al Jadeed'

    def get_logo(self) -> str:
        return 'http://www.aljadeed.tv/images/logo.png'

    def get_stream_url(self) -> str:
        return stream.fetch_from('http://live.aljadeed.tv/aljadeed/index-1.php')

    def get_epg_data(self):
        return fetch_epg('http://www.aljadeed.tv/arabic/programs/schedule', JadeedParser())
