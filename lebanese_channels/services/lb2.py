import datetime
from typing import List

from lebanese_channels.channel import Channel
from lebanese_channels.epg.program_data import ProgramData
from lebanese_channels.services.epg_parsers.lbc_parser import LBCParser
from lebanese_channels.services.utils.epg import fetch_epg


class LB2(Channel):
    def get_name(self) -> str:
        return 'LB2'

    def get_logo(self) -> str:
        return 'https://pbs.twimg.com/profile_images/776806340790476800/CMdKBI7R_400x400.jpg'

    def get_stream_url(self) -> str:
        return 'https://svs.itworkscdn.net/lbcdramalive/drama/playlist.m3u8'

    def get_epg_data(self) -> List[ProgramData]:
        now = datetime.datetime.now()

        today = now.strftime('%Y/%m/%d')
        tomorrow = (now + datetime.timedelta(days=1)).strftime('%Y/%m/%d')
        after_tomorrow = (now + datetime.timedelta(days=2)).strftime('%Y/%m/%d')

        urls = ['https://www.lbcgroup.tv/schedule-channels-date/9/' + today + '/ar',
                'https://www.lbcgroup.tv/schedule-channels-date/9/' + tomorrow + '/ar',
                'https://www.lbcgroup.tv/schedule-channels-date/9/' + after_tomorrow + '/ar']

        data = []
        for url in urls:
            epg = fetch_epg(url, LBCParser())
            data.extend(epg)

        return data
