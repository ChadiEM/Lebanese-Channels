from typing import List

from lebanese_channels.epg.epg_data import EPGData
from lebanese_channels.epg.epg_url import EPGURL


class JadeedEPGData(EPGData):
    @staticmethod
    def get_fetch_urls() -> List[EPGURL]:
        return [EPGURL('http://www.aljadeed.tv/arabic/programs/schedule')]

    @staticmethod
    def get_normalization() -> str:
        return 'نشرة الاخبار المسائية'
