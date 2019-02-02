from typing import List

from lebanese_channels.channel import CheckedChannel
from lebanese_channels.epg.program_data import ProgramData


class MTV(CheckedChannel):
    def get_name(self) -> str:
        return 'MTV'

    def get_logo(self) -> str:
        return 'http://mtv.com.lb/Content/images/logo-header.jpg'

    def get_stream_url(self) -> str:
        return 'https://svs.itworkscdn.net/mtvlebanonlive/mtvlive.smil/playlist.m3u8'

    def get_epg_data(self) -> List[ProgramData]:
        return None
