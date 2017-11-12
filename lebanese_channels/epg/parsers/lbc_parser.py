import datetime
import re

import bs4

from lebanese_channels.epg.epg_parser import EPGParser
from lebanese_channels.epg.program_data import ProgramData


class LBCParser(EPGParser):
    @staticmethod
    def parse_schedule_page(page_data: str):
        data = []
        parsed_html = bs4.BeautifulSoup(page_data, 'lxml')

        url = parsed_html.find('link', attrs={'rel': 'canonical'})['href']
        split_url = url.split('/')

        year = int(split_url[-4])
        month = int(split_url[-3])
        day = int(split_url[-2])

        listings = parsed_html.find_all('table', attrs={'class': 'ScheduleMoreThan452'})

        for listing in listings:
            title = listing.find('h2').find('a').text.strip()
            time_string = listing.find('span', attrs={'class': 'FromTimeSchedule'}).text
            hour = int(time_string.split(':')[0])
            minute = int(time_string.split(':')[1])

            duration_string = listing.find('h6', attrs={'class': 'AktivGrotesk_W_Rg'}).text
            duration = int(re.findall(r'\d+', duration_string)[0])

            description = listing.find('h5', attrs={'class': 'AktivGrotesk_W_Rg'}).text

            start_time = datetime.datetime(year, month, day, hour, minute)
            end_time = start_time + datetime.timedelta(minutes=duration)

            data.append(ProgramData(title, start_time, end_time, desc=description))

        return data
