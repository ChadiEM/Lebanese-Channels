import datetime
from typing import List

from program_data import ProgramData


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
        if match in program_data.name:
            hr = program_data.start_time.hour
            shift = 18 - hr
            break

    for program_data in program_data_list:
        program_data.shift_to_paris_time(shift)
