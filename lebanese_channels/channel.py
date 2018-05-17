import re
from abc import ABC, abstractmethod
from typing import List

from lebanese_channels.epg.program_data import ProgramData


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

    @abstractmethod
    def get_epg_data(self) -> List[ProgramData]:
        pass

    def get_route_name(self) -> str:
        return re.sub(r'\W+', '', self.get_name()).lower()

    def is_available(self) -> bool:
        return True


class CheckedChannel(Channel, ABC):
    def is_available(self) -> bool:
        try:
            self.get_stream_url()
            return True
        except StreamNotFoundError:
            return False
        except:
            # We don't know, return True
            return True


class StreamError(Exception):
    def __init__(self, url):
        self._url = url


class StreamNotFoundError(Exception):
    def __init__(self, url):
        self._url = url
