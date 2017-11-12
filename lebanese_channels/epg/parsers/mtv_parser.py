import datetime
import json
import re

from lebanese_channels.epg import epg_utils
from lebanese_channels.epg.epg_parser import EPGParser
from lebanese_channels.epg.program_data import ProgramData


class MTVParser(EPGParser):
    @staticmethod
    def parse_schedule_page(page_data: str):
        data = []

        json_parsed = json.loads(page_data)

        date_string = json_parsed[0]['date']
        splitted_date = date_string.split('/')

        month = int(splitted_date[0])
        day = int(splitted_date[1])
        year = int(splitted_date[2])

        for program in json_parsed[0]['programs']:
            name = program['programName']
            program_description = program['description']

            if program_description is not None:
                description = re.sub(r'<[^<>]+>', '', program_description).strip()
                description = re.sub(r'[\n\r]+', ' ', description)
            else:
                description = None

            category = program['category']

            icon = program['image']

            time_string = program['time']
            hour = int(time_string.split(':')[0])
            minute = int(time_string.split(':')[1])

            start_time = datetime.datetime(year, month, day, hour, minute)

            data.append(ProgramData(name, start_time, desc=description, category=category, icon=icon))

        epg_utils.fill_end_times(data)

        return data
