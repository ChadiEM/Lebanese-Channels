import abc
import datetime
from typing import List


class PostURL(object):
    def __init__(self, url, params):
        self.url = url
        self.params = params


class EPGData(metaclass=abc.ABCMeta):
    @staticmethod
    def get_fetch_urls() -> List[str]:
        return []

    @staticmethod
    def get_post_url() -> PostURL:
        return None

    @staticmethod
    @abc.abstractmethod
    def get_normalization() -> str:
        return ''


class LBCEPGData(EPGData):
    @staticmethod
    def get_fetch_urls() -> List[str]:
        today = datetime.datetime.now().strftime('%Y/%m/%d')
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y/%m/%d')
        after_tomorrow = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y/%m/%d')

        return ['https://www.lbcgroup.tv/schedule-channels-date/5/' + today + '/ar',
                'https://www.lbcgroup.tv/schedule-channels-date/5/' + tomorrow + '/ar',
                'https://www.lbcgroup.tv/schedule-channels-date/5/' + after_tomorrow + '/ar']

    @staticmethod
    def get_normalization() -> str:
        return 'نشرة الأخبار المسائية'


class LB2EPGData(EPGData):
    @staticmethod
    def get_fetch_urls() -> List[str]:
        today = datetime.datetime.now().strftime('%Y/%m/%d')
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y/%m/%d')
        after_tomorrow = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y/%m/%d')

        return ['https://www.lbcgroup.tv/schedule-channels-date/9/' + today + '/ar',
                'https://www.lbcgroup.tv/schedule-channels-date/9/' + tomorrow + '/ar',
                'https://www.lbcgroup.tv/schedule-channels-date/9/' + after_tomorrow + '/ar']

    @staticmethod
    def get_normalization() -> str:
        return None


class MTVEPGData(EPGData):
    @staticmethod
    def get_fetch_urls() -> List[str]:
        today = datetime.datetime.now().strftime('%a')
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%a')
        after_tomorrow = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%a')
        return ['http://mtv.com.lb/program/getDayGridByDayName?dayName=' + today,
                'http://mtv.com.lb/program/getDayGridByDayName?dayName=' + tomorrow,
                'http://mtv.com.lb/program/getDayGridByDayName?dayName=' + after_tomorrow]

    @staticmethod
    def get_normalization() -> str:
        return 'Prime Time News'


class JadeedEPGData(EPGData):
    @staticmethod
    def get_fetch_urls() -> List[str]:
        return ['http://www.aljadeed.tv/arabic/programs/schedule']

    @staticmethod
    def get_normalization() -> str:
        return 'نشرة الاخبار المسائية'


class NoursatEPGData(EPGData):
    @staticmethod
    def get_post_url() -> PostURL:
        week_number = str(datetime.datetime.today().isocalendar()[1])

        return PostURL('http://noursat.tv/ajax/tvProgramsFc.php',
                       {'action': 'LoadTvGridByChannel',
                        'channelId': '2',
                        'weekNumber': week_number,
                        'showFullGrid': '1'})

    @staticmethod
    def get_normalization() -> str:
        return 'النشرة'
