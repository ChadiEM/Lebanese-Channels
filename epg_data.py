import abc
import datetime


class EPGData(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_fetch_url(self):
        return


class LBCEPGData(EPGData):
    def get_fetch_url(self):
        return 'http://www.lbcgroup.tv/schedule-channels/5/lbc-europe-cet-time-paris/ar'


class MTVEPGData(EPGData):
    def get_fetch_url(self):
        today = datetime.datetime.now().strftime('%a')
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%a')
        after_tomorrow = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%a')
        return ['http://mtv.com.lb/program/getDayGridByDayName?dayName=' + today,
                'http://mtv.com.lb/program/getDayGridByDayName?dayName=' + tomorrow,
                'http://mtv.com.lb/program/getDayGridByDayName?dayName=' + after_tomorrow]


class OTVEPGData(EPGData):
    def get_fetch_url(self):
        today = str(datetime.datetime.today().weekday() + 1)
        tomorrow = str((datetime.datetime.today() + datetime.timedelta(days=1)).weekday() + 1)
        after_tomorrow = str((datetime.datetime.today() + datetime.timedelta(days=2)).weekday() + 1)
        return ['http://www.otv.com.lb/beta/_ajax.php?action=grid&id=' + today + '&r=14',
                'http://www.otv.com.lb/beta/_ajax.php?action=grid&id=' + tomorrow + '&r=14',
                'http://www.otv.com.lb/beta/_ajax.php?action=grid&id=' + after_tomorrow + '&r=14']


class JadeedEPGData(EPGData):
    def get_fetch_url(self):
        return 'http://www.aljadeed.tv/arabic/programs/schedule'
