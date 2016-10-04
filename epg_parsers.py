import abc
import datetime
import json
import re

import bs4


class EPGParser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse(self, page_data):
        return


class LBCParser(EPGParser):
    def parse(self, page_data):
        processed_data = []
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

            start_time = datetime.datetime.now().replace(hour=hr, minute=min, second=0, microsecond=0)
            if next_day_show:
                start_time = start_time + datetime.timedelta(days=1)
            end_time = start_time + datetime.timedelta(minutes=duration)

            processed_data.append([title, start_time, end_time])

        return calibrate(processed_data, 'نشرة الأخبار المسائية')


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

            time_string = program['time']
            hr = int(time_string.split(':')[0])
            min = int(time_string.split(':')[1])

            start_time = datetime.datetime(year, month, day, hr, min)

            data.append([name, start_time])

        processed_data = append_end_times(data)

        return calibrate(processed_data, 'Prime Time News')


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

            data.append([title, start_time])

        processed_data = append_end_times(data)

        return calibrate(processed_data, 'News 19:45')


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
            data.append([title, start_time])

        processed_data = append_end_times(data)

        return calibrate(processed_data, 'نشرة الاخبار المسائية')


def append_end_times(start_datas):
    processed_data = []

    index = 0
    for start_data in start_datas:
        if index + 1 >= len(start_datas):
            finish_date = start_data[1] + datetime.timedelta(minutes=60)
        else:
            finish_date = start_datas[index + 1][1]
        processed_data.append([start_data[0], start_data[1], finish_date])
        index += 1

    return processed_data


def calibrate(processed_data, match):
    updated_processed_data = []

    shift = 0
    for current_data in processed_data:
        if match in current_data[0]:
            hr = current_data[1].hour
            shift = 18 - hr
            break

    for current_data in processed_data:
        updated_processed_data.append([current_data[0], current_data[1] + datetime.timedelta(hours=shift),
                                       current_data[2] + datetime.timedelta(hours=shift)])

    return updated_processed_data
