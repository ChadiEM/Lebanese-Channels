import datetime
from typing import List
from urllib.error import HTTPError
from xml.etree import ElementTree

from lebanese_channels.channel import Channel, StreamError
from lebanese_channels.epg.program_data import ProgramData
from lebanese_channels.services.epg_parsers.lbc_parser import LBCParser
from lebanese_channels.services.utils.epg import fetch_epg
from lebanese_channels.services.utils.web import get_response


class LBC(Channel):
    def get_name(self) -> str:
        return 'LBC'

    def get_logo(self) -> str:
        return 'http://www.lbcgroup.tv/programsimages/PCL-5-635531118011703749.png'

    def get_stream_url(self) -> str:
        try:
            html = get_response('http://mobilefeeds.lbcgroup.tv/getCategories.aspx')
        except HTTPError:
            raise StreamError('lbc')

        root = ElementTree.fromstring(html)
        playlist = root.find('watchLive')
        if playlist is not None:
            return playlist.text

        raise StreamError('lbc')

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
