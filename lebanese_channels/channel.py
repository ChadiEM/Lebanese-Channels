import re
from abc import ABC, abstractmethod


class Channel(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_logo(self) -> str:
        pass

    @abstractmethod
    def get_stream_url(self) -> str:
        pass

    def get_route_name(self) -> str:
        return re.sub(r'\W+', '', self.get_name()).lower()


class StreamError(Exception):
    def __init__(self, url):
        self._url = url


class StreamNotFoundError(Exception):
    def __init__(self, url):
        self._url = url
