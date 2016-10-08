import abc
import datetime
import json
import re
from typing import Dict

import bs4

import epg_utils
import utils
from program_data import ProgramData


class EPGParser(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def parse_schedule_page(page_data: str):
        return


class LBCParser(EPGParser):
    @staticmethod
    def parse_schedule_page(page_data: str):
        data = []
        parsed_html = bs4.BeautifulSoup(page_data, 'lxml')

        listings = parsed_html.find_all('table', attrs={'class': 'ScheduleMoreThan452'})

        for listing in listings:
            next_day_show = False
            main_div = listing.parent.parent
            if main_div.name == 'div':
                previous_siblings = main_div.previous_siblings

                for sibling in previous_siblings:
                    if sibling.name == 'div' and sibling.has_attr('id') and 'DivShowNextDate' in sibling['id']:
                        next_day_show = True

            title = listing.find('h2').find('a').text.strip()
            time_string = listing.find('span', attrs={'class': 'FromTimeSchedule'}).text
            hr = int(time_string.split(':')[0])
            min = int(time_string.split(':')[1])

            duration_string = listing.find('h6', attrs={'class': 'AktivGrotesk_W_Rg'}).text
            duration = int(re.findall(r'\d+', duration_string)[0])

            description = listing.find('h5', attrs={'class': 'AktivGrotesk_W_Rg'}).text

            start_time = datetime.datetime.now().replace(hour=hr, minute=min, second=0, microsecond=0)
            if next_day_show:
                start_time = start_time + datetime.timedelta(days=1)
            end_time = start_time + datetime.timedelta(minutes=duration)

            data.append(ProgramData(title, start_time, end_time, desc=description))

        return data


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
            description = re.sub('<[^<>]+>', '', program['description']).strip()
            description = re.sub('[\n\r]+', ' ', description)

            category = program['category']

            icon = program['image']

            time_string = program['time']
            hr = int(time_string.split(':')[0])
            min = int(time_string.split(':')[1])

            start_time = datetime.datetime(year, month, day, hr, min)

            data.append(ProgramData(name, start_time, desc=description, category=category, icon=icon))

        epg_utils.fill_end_times(data)

        return data


class OTVParser(EPGParser):
    @staticmethod
    def parse_schedule_page(page_data: str):
        data = []
        additional_mappings = dict()

        date = datetime.datetime.strptime(page_data.split('|@|')[1], '%a, %d %b %Y')

        parsed_html = bs4.BeautifulSoup(page_data, 'lxml')
        listings = parsed_html.find_all('li')

        for listing in listings:
            title = listing.find('div', attrs={'class': 'b2'}).find('h3').text
            time_string = listing.find('div', attrs={'class': 'b3'}).find('span').text.split()[0]
            time_string_split = time_string.split(':')
            hr = int(time_string_split[0])
            min = int(time_string_split[1])

            start_time = datetime.datetime(date.year, date.month, date.day, hr, min)

            program_data = ProgramData(title, start_time)

            program_url = listing.find('div', attrs={'class': 'b1'}).a['href']
            # if is_ascii(program_url): #urllib3 doens't work with non-ascii urls!
            additional_mappings[program_data] = program_url

            data.append(program_data)

        epg_utils.fill_end_times(data)
        # fill_otv_additional_data(additional_mappings)

        return data


# def fill_otv_additional_data(additional_mappings: Dict[ProgramData, str]):
#     for program_data, url in additional_mappings.items():
#         print(url)
#
#         html = utils.get_html_response_for(url)
#         print(html)
#         parsed_html = bs4.BeautifulSoup(html, 'html.parser')
#
#
#         desc_div = parsed_html.find('div', attrs={'class': 'epitop'})
#         print(desc_div)
#         program_data.set_desc(desc_div.h3.text)
#
#
# def is_ascii(s):
#     return all(ord(c) < 128 for c in s)


class JadeedParser(EPGParser):
    @staticmethod
    def parse_schedule_page(page_data: str):
        data = []
        additional_mappings = dict()
        parsed_html = bs4.BeautifulSoup(page_data, 'lxml')
        listing = parsed_html.body.find('div', attrs={'class': 'programListing'})
        rows = listing.find_all('div', attrs={'class': 'listingRow'})

        for row in rows:
            title = re.sub('<.*?>', '', row.find('div', attrs={'class': 'listingTitle'}).text.strip())
            time_string = re.sub('<.*?>', '', row.find('div', attrs={'class': 'listingDate'}).text.strip())
            time_string_split = time_string.split(':')
            hr = int(time_string_split[0])
            min = int(time_string_split[1])

            links_div = row.find('div', attrs={'class': 'listingLink'})
            page_url_anchor = links_div.find_all('a')[1]
            program_id = page_url_anchor['href'].split('=')[1]

            start_time = datetime.datetime.now().replace(hour=hr, minute=min, second=0, microsecond=0)
            program_data = ProgramData(title, start_time)
            data.append(program_data)

            additional_mappings[program_data] = 'http://aljadeed.tv/arabic/about-program?programid=' + program_id

        epg_utils.fill_end_times(data)
        fill_jadeed_additional_mappings(additional_mappings)

        return data


def fill_jadeed_additional_mappings(additional_mappings: Dict[ProgramData, str]):
    for program_data, url in additional_mappings.items():
        html = utils.get_html_response_for(url)
        parsed_html = bs4.BeautifulSoup(html, 'lxml')

        image_div = parsed_html.find('div', attrs={'class': 'mainArtistImage'})
        image_src = 'http://aljadeed.tv' + image_div.img['src']
        program_data.set_icon(image_src)

        text_div = parsed_html.find('div', attrs={'class': 'newsContent'})
        program_data.set_desc(text_div.text)
