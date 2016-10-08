import abc
import datetime


class EPGData(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def get_fetch_url():
        return

    @staticmethod
    @abc.abstractmethod
    def get_normalization() -> str:
        return


class LBCEPGData(EPGData):
    @staticmethod
    def get_fetch_url():
        return 'http://www.lbcgroup.tv/schedule-channels/5/lbc-europe-cet-time-paris/ar'

    @staticmethod
    def get_normalization() -> str:
        return 'نشرة الأخبار المسائية'


class MTVEPGData(EPGData):
    @staticmethod
    def get_fetch_url():
        today = datetime.datetime.now().strftime('%a')
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%a')
        after_tomorrow = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%a')
        return ['http://mtv.com.lb/program/getDayGridByDayName?dayName=' + today,
                'http://mtv.com.lb/program/getDayGridByDayName?dayName=' + tomorrow,
                'http://mtv.com.lb/program/getDayGridByDayName?dayName=' + after_tomorrow]

    @staticmethod
    def get_normalization() -> str:
        return 'Prime Time News'


class OTVEPGData(EPGData):
    @staticmethod
    def get_fetch_url():
        today = str(datetime.datetime.today().weekday() + 1)
        tomorrow = str((datetime.datetime.today() + datetime.timedelta(days=1)).weekday() + 1)
        after_tomorrow = str((datetime.datetime.today() + datetime.timedelta(days=2)).weekday() + 1)
        return ['http://www.otv.com.lb/beta/_ajax.php?action=grid&id=' + today + '&r=14',
                'http://www.otv.com.lb/beta/_ajax.php?action=grid&id=' + tomorrow + '&r=14',
                'http://www.otv.com.lb/beta/_ajax.php?action=grid&id=' + after_tomorrow + '&r=14']

    @staticmethod
    def get_normalization() -> str:
        return 'News 19:45'


class JadeedEPGData(EPGData):
    @staticmethod
    def get_fetch_url():
        return 'http://www.aljadeed.tv/arabic/programs/schedule'

    @staticmethod
    def get_normalization() -> str:
        return 'نشرة الاخبار المسائية'
