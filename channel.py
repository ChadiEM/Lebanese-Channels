from epg_data import EPGData
from epg_parsers import EPGParser


class Channel(object):
    def __init__(self, channel_id, name, logo, stream_url=None, route=None, epg_data=None, epg_parser=None):
        self.channel_id = channel_id
        self.name = name
        self.logo = logo
        self.url = stream_url
        self.route = route
        self.epg_data = epg_data
        self.epg_parser = epg_parser

    def get_channel_id(self):
        return self.channel_id

    def get_name(self):
        return self.name

    def get_logo(self):
        return self.logo

    def get_url(self):
        return self.url

    def get_route(self):
        return self.route

    def get_epg_data(self) -> EPGData:
        return self.epg_data

    def get_epg_parser(self) -> EPGParser:
        return self.epg_parser
