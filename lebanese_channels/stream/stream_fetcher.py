import abc


class StreamFetcher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_route_name(self) -> str:
        return ''

    @abc.abstractmethod
    def fetch_stream_url(self) -> str:
        return ''


class StreamError(Exception):
    def __init__(self, url):
        self.channel = url
