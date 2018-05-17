from abc import ABC, abstractmethod


class EPGParser(ABC):
    @staticmethod
    @abstractmethod
    def parse_schedule_page(page_data: str):
        return
