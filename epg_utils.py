import datetime
from typing import List

from program_data import ProgramData


def fill_end_times(program_datas: List[ProgramData]):
    index = 0
    for program_data in program_datas:
        if index + 1 >= len(program_datas):
            finish_date = program_data.get_start_time() + datetime.timedelta(minutes=60)
        else:
            finish_date = program_datas[index + 1].get_start_time()

        program_data.set_stop_time(finish_date)

        index += 1


def normalize_times(program_data_list: List[ProgramData], match: str):
    shift = 0
    for program_data in program_data_list:
        if match in program_data.get_name():
            hr = program_data.get_start_time().hour
            shift = 18 - hr
            break

    for program_data in program_data_list:
        program_data.shift_to_paris_time(shift)
