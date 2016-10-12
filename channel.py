from typing import List

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
                 not_available_in: List[str] = None,
                 epg_data: EPGData = None,
                 epg_parser: EPGParser = None):
        self._channel_id = channel_id
        self._name = name
        self._logo = logo
        self._url = stream_url
        self._stream_fetcher = stream_fetcher
        self._not_available_in = not_available_in
        self._epg_data = epg_data
        self._epg_parser = epg_parser

    @property
    def channel_id(self) -> int:
        return self._channel_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def logo(self) -> str:
        return self._logo

    @property
    def url(self) -> str:
        return self._url

    @property
    def stream_fetcher(self) -> StreamFetcher:
        return self._stream_fetcher

    @property
    def epg_data(self) -> EPGData:
        return self._epg_data

    @property
    def epg_parser(self) -> EPGParser:
        return self._epg_parser

    def available_in(self, location: str) -> bool:
        return (self._not_available_in is None) or (location not in self._not_available_in)
