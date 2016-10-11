import datetime

import pytz


class ProgramData(object):
    def __init__(self, name: str, start_time: datetime, stop_time: datetime = None, desc: str = None,
                 category: str = None, icon: str = None):
        self._name = name
        self._start_time = start_time
        self._stop_time = stop_time
        self._desc = desc
        self._category = category
        self._icon = icon

    @property
    def name(self) -> str:
        return self._name

    @property
    def start_time(self) -> datetime:
        return self._start_time

    @property
    def stop_time(self) -> datetime:
        return self._stop_time

    @property
    def category(self) -> str:
        return self._category

    @property
    def desc(self) -> str:
        return self._desc

    @property
    def icon(self) -> str:
        return self._icon

    @stop_time.setter
    def stop_time(self, stop_time: datetime):
        self._stop_time = stop_time

    @desc.setter
    def desc(self, desc: str):
        self._desc = desc

    @icon.setter
    def icon(self, icon: str):
        self._icon = icon

    def shift_to_paris_time(self, hours):
        shift = datetime.timedelta(hours=hours)
        self._start_time = self._start_time + shift
        self._stop_time = self._stop_time + shift

        paris_time = datetime.datetime.now(pytz.timezone('Europe/Paris'))
        self._start_time = self._start_time.replace(tzinfo=paris_time.tzinfo)
        self._stop_time = self._stop_time.replace(tzinfo=paris_time.tzinfo)
