import abc
from typing import List


class PostURL(object):
    def __init__(self, url, params):
        self.url = url
        self.params = params


class EPGData(metaclass=abc.ABCMeta):
    @staticmethod
    def get_fetch_urls() -> List[str]:
        return []

    @staticmethod
    @abc.abstractmethod
    def get_normalization() -> str:
        return ''
