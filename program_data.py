import datetime


class ProgramData(object):
    def __init__(self, name, start_time, stop_time=None, desc=None, category=None):
        self.name = name
        self.start_time = start_time
        self.stop_time = stop_time
        self.desc = desc
        self.category = category

    def get_name(self):
        return self.name

    def get_start_time(self):
        return self.start_time

    def get_stop_time(self):
        return self.stop_time

    def shift(self, hours):
        shift = datetime.timedelta(hours=hours)
        self.start_time = self.start_time + shift
        self.stop_time = self.stop_time + shift

    def set_stop_time(self, stop_time):
        self.stop_time = stop_time

    def get_desc(self):
        return self.desc

    def get_category(self):
        return self.category
