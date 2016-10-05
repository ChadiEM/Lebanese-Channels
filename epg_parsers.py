import abc
import datetime
import json
import re

import bs4

from program_data import ProgramData


class EPGParser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse(self, page_data):
        return


class LBCParser(EPGParser):
    def parse(self, page_data):
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

        calibrate(data, 'نشرة الأخبار المسائية')

        return data


class MTVParser(EPGParser):
    def parse(self, page_data):
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

            time_string = program['time']
            hr = int(time_string.split(':')[0])
            min = int(time_string.split(':')[1])

            start_time = datetime.datetime(year, month, day, hr, min)

            data.append(ProgramData(name, start_time, desc=description, category=category))

        fill_end_times(data)
        calibrate(data, 'Prime Time News')

        return data


class OTVParser(EPGParser):
    def parse(self, page_data):
        data = []

        date = datetime.datetime.strptime(page_data.split('|@|')[1], '%a, %d %b %Y')

        parsed_html = bs4.BeautifulSoup(page_data, 'lxml')
        listings = parsed_html.find_all('li')

        for listing in listings:
            title = listing.find('div', attrs={'class': 'b2'}).find('h3').text
            time_string = listing.find('div', attrs={'class': 'b3'}).find('span').text.split()[0]
            hr = int(time_string.split(':')[0])
            min = int(time_string.split(':')[1])

            start_time = datetime.datetime(date.year, date.month, date.day, hr, min)

            data.append(ProgramData(title, start_time))

        fill_end_times(data)
        calibrate(data, 'News 19:45')

        return data


class JadeedParser(EPGParser):
    def parse(self, page_data):
        data = []
        parsed_html = bs4.BeautifulSoup(page_data, 'lxml')
        listing = parsed_html.body.find('div', attrs={'class': 'programListing'})
        rows = listing.find_all('div', attrs={'class': 'listingRow'})

        for row in rows:
            title = re.sub('<.*?>', '', row.find('div', attrs={'class': 'listingTitle'}).text.strip())
            time_string = re.sub('<.*?>', '', row.find('div', attrs={'class': 'listingDate'}).text.strip())
            hr = int(time_string.split(':')[0])
            min = int(time_string.split(':')[1])

            start_time = datetime.datetime.now().replace(hour=hr, minute=min, second=0, microsecond=0)
            data.append(ProgramData(title, start_time))

        fill_end_times(data)
        calibrate(data, 'نشرة الاخبار المسائية')

        return data


def fill_end_times(program_datas):
    index = 0
    for program_data in program_datas:
        if index + 1 >= len(program_datas):
            finish_date = program_data.get_start_time() + datetime.timedelta(minutes=60)
        else:
            finish_date = program_datas[index + 1].get_start_time()

        program_data.set_stop_time(finish_date)

        index += 1


def calibrate(program_datas, match):
    shift = 0
    for program_data in program_datas:
        if match in program_data.get_name():
            hr = program_data.get_start_time().hour
            shift = 18 - hr
            break

    for program_data in program_datas:
        program_data.shift(shift)
