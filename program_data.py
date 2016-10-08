import datetime

import pytz


class ProgramData(object):
    def __init__(self, name: str, start_time: datetime, stop_time=None, desc=None, category=None, icon=None):
        self.name = name
        self.start_time = start_time
        self.stop_time = stop_time
        self.desc = desc
        self.category = category
        self.icon = icon

    def get_name(self) -> str:
        return self.name

    def get_start_time(self) -> datetime:
        return self.start_time

    def get_stop_time(self) -> datetime:
        return self.stop_time

    def shift_to_paris_time(self, hours):
        shift = datetime.timedelta(hours=hours)
        self.start_time = self.start_time + shift
        self.stop_time = self.stop_time + shift

        paris_time = datetime.datetime.now(pytz.timezone('Europe/Paris'))
        self.start_time = self.start_time.replace(tzinfo=paris_time.tzinfo)
        self.stop_time = self.stop_time.replace(tzinfo=paris_time.tzinfo)

    def set_stop_time(self, stop_time: datetime):
        self.stop_time = stop_time

    def get_category(self) -> str:
        return self.category

    def get_desc(self) -> str:
        return self.desc

    def set_desc(self, desc: str):
        self.desc = desc

    def get_icon(self) -> str:
        return self.icon

    def set_icon(self, icon: str):
        self.icon = icon
