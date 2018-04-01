import abc


class EPGParser(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def parse_schedule_page(page_data: str):
        return
