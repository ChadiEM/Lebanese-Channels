import abc
import datetime
import json
import re

import bs4


class EPGParser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse(self, page_data, shift):
        return

    def process_data(self, data, shift):
        processed_data = []
        today = datetime.datetime.now().strftime('%Y%m%d')
        tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y%m%d')

        index = 0
        for data_row in data:
            start_time = str(int(data_row[1]) + shift).zfill(4)
            if index + 1 >= len(data):
                end_datetime = tomorrow + '0000'
            else:
                end_datetime = today + str(int(data[index + 1][1]) + shift).zfill(4)

            if int(start_time) >= 0:
                start = today + start_time + '00 +0100'
                end = end_datetime + '00 +0100'
                title = data_row[0]
                processed_data.append([start, end, title])
            index += 1

        return processed_data


class LBCParser(EPGParser):
    def parse(self, page_data, shift):
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

            if not next_day_show:
                title = listing.find('h2').find('a').text.strip()
                date = listing.find('span', attrs={'class': 'FromTimeSchedule'}).text.replace(':', '')
                data.append([title, date])

        return self.process_data(data, shift)


class MTVParser(EPGParser):
    def parse(self, page_data, shift):
        data = []

        json_parsed = json.loads(page_data)

        for program in json_parsed[0]['programs']:
            name = program['programName']
            time = program['time'].replace(':', '')
            data.append([name, time])

        return self.process_data(data, shift)


class OTVParser(EPGParser):
    def parse(self, page_data, shift):
        data = []
        parsed_html = bs4.BeautifulSoup(page_data, 'lxml')
        listings = parsed_html.find_all('li')

        for listing in listings:
            title = listing.find('div', attrs={'class': 'b2'}).find('h3').text
            date = listing.find('div', attrs={'class': 'b3'}).find('span').text.split()[0].replace(':', '')

            data.append([title, date])

        return self.process_data(data, shift)


class JadeedParser(EPGParser):
    def parse(self, page_data, shift):
        data = []
        parsed_html = bs4.BeautifulSoup(page_data, 'lxml')
        listing = parsed_html.body.find('div', attrs={'class': 'programListing'})
        rows = listing.find_all('div', attrs={'class': 'listingRow'})

        for row in rows:
            title = re.sub('<.*?>', '', row.find('div', attrs={'class': 'listingTitle'}).text.strip())
            date = re.sub('<.*?>', '', row.find('div', attrs={'class': 'listingDate'}).text.strip()).replace(':', '')
            data.append([title, date])

        return self.process_data(data, shift)
