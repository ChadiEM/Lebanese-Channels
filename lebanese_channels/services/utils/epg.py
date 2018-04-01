import datetime
from typing import List

from lebanese_channels.epg.program_data import ProgramData
from lebanese_channels.services.epg_parsers.epg_parser import EPGParser
from lebanese_channels.services.utils import web


def fetch_epg(url: str, parser: EPGParser):
    html = web.get_response(url)
    return fetch_epg_from_page(html, parser)


def fetch_epg_from_page(page_data: str, parser: EPGParser):
    start_end_data = parser.parse_schedule_page(page_data)
    return start_end_data


def fill_end_times(program_data_list: List[ProgramData]):
    index = 0
    for program_data in program_data_list:
        if index + 1 >= len(program_data_list):
            finish_date = program_data.start_time + datetime.timedelta(minutes=60)
        else:
            finish_date = program_data_list[index + 1].start_time

        program_data.stop_time = finish_date

        index += 1
