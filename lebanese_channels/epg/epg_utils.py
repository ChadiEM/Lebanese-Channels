import datetime
from typing import List

from lebanese_channels.epg.program_data import ProgramData


def fill_end_times(program_data_list: List[ProgramData]):
    index = 0
    for program_data in program_data_list:
        if index + 1 >= len(program_data_list):
            finish_date = program_data.start_time + datetime.timedelta(minutes=60)
        else:
            finish_date = program_data_list[index + 1].start_time

        program_data.stop_time = finish_date

        index += 1


def normalize_times(program_data_list: List[ProgramData], match: str):
    shift = 0
    for program_data in program_data_list:
        if match is not None and match in program_data.name:
            hour = program_data.start_time.hour
            shift = 18 - hour
            break

    for program_data in program_data_list:
        program_data.shift_to_paris_time(shift)
