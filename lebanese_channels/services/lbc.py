import datetime
from typing import List

from lebanese_channels.channel import CheckedChannel
from lebanese_channels.epg.program_data import ProgramData
from lebanese_channels.services.epg_parsers.lbc_parser import LBCParser
from lebanese_channels.services.utils import stream
from lebanese_channels.services.utils.epg import fetch_epg


class LBC(CheckedChannel):
    def get_name(self) -> str:
        return 'LBC'

    def get_logo(self) -> str:
        return 'https://www.lbcgroup.tv/programsimages/Channels-L-1-636090059981705970.png'

    def get_stream_url(self) -> str:
        return stream.fetch_from('https://www.lbcgroup.tv/live/en')

    def get_epg_data(self) -> List[ProgramData]:
        now = datetime.datetime.now()

        today = now.strftime('%Y/%m/%d')
        tomorrow = (now + datetime.timedelta(days=1)).strftime('%Y/%m/%d')
        after_tomorrow = (now + datetime.timedelta(days=2)).strftime('%Y/%m/%d')

        urls = ['https://www.lbcgroup.tv/schedule-channels-date/5/' + today + '/ar',
                'https://www.lbcgroup.tv/schedule-channels-date/5/' + tomorrow + '/ar',
                'https://www.lbcgroup.tv/schedule-channels-date/5/' + after_tomorrow + '/ar']

        data = []
        for url in urls:
            epg = fetch_epg(url, LBCParser())
            data.extend(epg)

        return data
