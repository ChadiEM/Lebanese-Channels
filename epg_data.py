import abc
import datetime


class EPGData(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_fetch_url(self):
        return

    @abc.abstractmethod
    def get_time_shift(self):
        return


class LBCEPGData(EPGData):
    def get_fetch_url(self):
        return 'http://www.lbcgroup.tv/schedule-channels-date/5/' + datetime.datetime.now().strftime('%Y/%m/%d') + '/ar'

    def get_time_shift(self):
        return 100


class MTVEPGData(EPGData):
    def get_fetch_url(self):
        return 'http://mtv.com.lb/program/getDayGridByDayName?dayName='

    def get_time_shift(self):
        return -100


class OTVEPGData(EPGData):
    def get_fetch_url(self):
        return 'http://www.otv.com.lb/beta/_ajax.php?action=grid&id=' + str(
            datetime.datetime.today().weekday() + 1) + '&r=14'

    def get_time_shift(self):
        return -100


class JadeedEPGData(EPGData):
    def get_fetch_url(self):
        return 'http://www.aljadeed.tv/arabic/programs/schedule'

    def get_time_shift(self):
        return -100
