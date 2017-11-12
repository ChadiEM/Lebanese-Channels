import datetime
from typing import List

from lebanese_channels.epg.epg_data import EPGData
from lebanese_channels.epg.epg_url import EPGURL


class MTVEPGData(EPGData):
    @staticmethod
    def get_fetch_urls() -> List[EPGURL]:
        today = datetime.datetime.now().strftime('%a')
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%a')
        after_tomorrow = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%a')

        return [EPGURL('http://mtv.com.lb/program/getDayGridByDayName?dayName=' + today),
                EPGURL('http://mtv.com.lb/program/getDayGridByDayName?dayName=' + tomorrow),
                EPGURL('http://mtv.com.lb/program/getDayGridByDayName?dayName=' + after_tomorrow)]

    @staticmethod
    def get_normalization() -> str:
        return 'Prime Time News'
