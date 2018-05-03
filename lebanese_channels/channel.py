import abc
import itertools
import re
from typing import List

from lebanese_channels.epg.program_data import ProgramData


class Channel(object):
    id_generator_function = itertools.count(start=1)

    def __init__(self):
        self._id = next(Channel.id_generator_function)

    @abc.abstractmethod
    def get_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_logo(self) -> str:
        pass

    @abc.abstractmethod
    def get_stream_url(self) -> str:
        pass

    @abc.abstractmethod
    def get_epg_data(self) -> List[ProgramData]:
        pass

    def get_route_name(self) -> str:
        return re.sub(r'\W+', '', self.get_name()).lower()

    def is_available(self) -> bool:
        return True

    @property
    def id(self) -> int:
        return self._id


class CheckedChannel(Channel):
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
