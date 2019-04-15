from typing import List

from lebanese_channels.channel import CheckedChannel
from lebanese_channels.epg.program_data import ProgramData
from lebanese_channels.services.utils import stream


class MTV(CheckedChannel):
    def get_name(self) -> str:
        return 'MTV'

    def get_logo(self) -> str:
        return 'http://mtv.com.lb/Content/images/logo-header.jpg'

    def get_stream_url(self) -> str:
        return stream.fetch_from('https://www.mtv.com.lb/Live/Player')

    def get_epg_data(self) -> List[ProgramData]:
        return None
