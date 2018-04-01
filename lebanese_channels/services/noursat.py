import datetime

from lebanese_channels.channel import Channel
from lebanese_channels.services.epg_parsers.noursat_parser import NoursatParser
from lebanese_channels.services.utils.epg import fetch_epg_from_page
from lebanese_channels.services.utils.web import get_response


class Noursat(Channel):
    def get_name(self) -> str:
        return 'Noursat'

    def get_logo(self) -> str:
        return 'http://noursat.tv/images/main-logo.png'

    def get_stream_url(self) -> str:
        return 'https://svs.itworkscdn.net/nour4satlive/livestream/playlist.m3u8'

    def get_epg_data(self):
        week_number = str(datetime.datetime.today().isocalendar()[1])

        url = 'http://noursat.tv/ajax/tvProgramsFc.php'
        params = {'action': 'LoadTvGridByChannel',
                  'channelId': '2',
                  'weekNumber': week_number,
                  'showFullGrid': '1'}

        page_data = get_response(url, params)

        return fetch_epg_from_page(page_data, NoursatParser())
