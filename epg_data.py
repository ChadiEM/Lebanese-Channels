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
        return 'http://mtv.com.lb/program/getDayGridByDayName?dayName='


class OTVEPGData(EPGData):
    def get_fetch_url(self):
        return 'http://www.otv.com.lb/beta/_ajax.php?action=grid&id=' + str(
            datetime.datetime.today().weekday() + 1) + '&r=14'


class JadeedEPGData(EPGData):
    def get_fetch_url(self):
        return 'http://www.aljadeed.tv/arabic/programs/schedule'
