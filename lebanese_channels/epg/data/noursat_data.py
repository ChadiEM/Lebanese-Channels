import datetime
from typing import List

from lebanese_channels.epg.epg_data import EPGData
from lebanese_channels.epg.epg_url import EPGURL


class NoursatEPGData(EPGData):
    @staticmethod
    def get_fetch_urls() -> List[EPGURL]:
        week_number = str(datetime.datetime.today().isocalendar()[1])

        return [EPGURL('http://noursat.tv/ajax/tvProgramsFc.php', {'action': 'LoadTvGridByChannel',
                                                                   'channelId': '2',
                                                                   'weekNumber': week_number,
                                                                   'showFullGrid': '1'})]

    @staticmethod
    def get_normalization() -> str:
        return 'النشرة'
