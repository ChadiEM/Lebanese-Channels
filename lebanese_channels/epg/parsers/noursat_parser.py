import datetime
import json

import bs4

from lebanese_channels.epg import epg_utils
from lebanese_channels.epg.epg_parser import EPGParser
from lebanese_channels.epg.program_data import ProgramData


class NoursatParser(EPGParser):
    @staticmethod
    def parse_schedule_page(page_data: str):
        data = []

        json_parsed = json.loads(page_data)
        html = json_parsed['fullGrid']

        parsed_html = bs4.BeautifulSoup(html, 'lxml')

        day_of_week = datetime.datetime.now().weekday()

        days = parsed_html.find_all('div', attrs={'class': 'day'})

        for day in days:
            program_day_number = int(day['id'].replace('grid', ''))
            shift = datetime.timedelta(days=program_day_number - day_of_week)

            programs = day.find_all('div', attrs={'class': 'program'})

            for program in programs:
                title = program.find('div', attrs={'class': 'title'}).text
                time_string = program.find('div', attrs={'class': 'time'}).text.split()[0]
                time_string_split = time_string.split(':')
                hour = int(time_string_split[0])
                minute = int(time_string_split[1])

                start_time = datetime.datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
                start_time = start_time + shift

                program_data = ProgramData(title, start_time)
                data.append(program_data)

        epg_utils.fill_end_times(data)

        return data
