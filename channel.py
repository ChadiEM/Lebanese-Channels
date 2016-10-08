from epg_data import EPGData
from epg_parsers import EPGParser
from stream_fetcher import StreamFetcher


class Channel(object):
    def __init__(self,
                 channel_id: int,
                 name: str,
                 logo: str,
                 stream_url: str = None,
                 stream_fetcher: StreamFetcher = None,
                 epg_data: EPGData = None,
                 epg_parser: EPGParser = None):
        self.channel_id = channel_id
        self.name = name
        self.logo = logo
        self.url = stream_url
        self.stream_fetcher = stream_fetcher
        self.epg_data = epg_data
        self.epg_parser = epg_parser

    def get_channel_id(self) -> int:
        return self.channel_id

    def get_name(self) -> str:
        return self.name

    def get_logo(self) -> str:
        return self.logo

    def get_url(self) -> str:
        return self.url

    def get_stream_fetcher(self) -> StreamFetcher:
        return self.stream_fetcher

    def get_epg_data(self) -> EPGData:
        return self.epg_data

    def get_epg_parser(self) -> EPGParser:
        return self.epg_parser
