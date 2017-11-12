import datetime
from typing import List

from lebanese_channels.epg.epg_data import EPGData
from lebanese_channels.epg.epg_url import EPGURL


class LBCEPGData(EPGData):
    @staticmethod
    def get_fetch_urls() -> List[EPGURL]:
        today = datetime.datetime.now().strftime('%Y/%m/%d')
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y/%m/%d')
        after_tomorrow = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y/%m/%d')

        return [EPGURL('https://www.lbcgroup.tv/schedule-channels-date/5/' + today + '/ar'),
                EPGURL('https://www.lbcgroup.tv/schedule-channels-date/5/' + tomorrow + '/ar'),
                EPGURL('https://www.lbcgroup.tv/schedule-channels-date/5/' + after_tomorrow + '/ar')]

    @staticmethod
    def get_normalization() -> str:
        return 'نشرة الأخبار المسائية'
