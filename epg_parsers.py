import abc
import json
import re

import bs4


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

            if not next_day_show:
                title = listing.find('h2').find('a').text.strip()
                date = listing.find('span', attrs={'class': 'FromTimeSchedule'}).text.replace(':', '')
                data.append([title, date])

        return data


class MTVParser(EPGParser):
    def parse(self, page_data):
        data = []

        json_parsed = json.loads(page_data)

        for program in json_parsed[0]['programs']:
            name = program['programName']
            time = program['time'].replace(':', '')
            data.append([name, time])

        return data


class OTVParser(EPGParser):
    def parse(self, page_data):
        data = []
        parsed_html = bs4.BeautifulSoup(page_data, 'lxml')
        listings = parsed_html.find_all('li')

        for listing in listings:
            title = listing.find('div', attrs={'class': 'b2'}).find('h3').text
            date = listing.find('div', attrs={'class': 'b3'}).find('span').text.split()[0].replace(':', '')

            data.append([title, date])

        return data


class JadeedParser(EPGParser):
    def parse(self, page_data):
        data = []
        parsed_html = bs4.BeautifulSoup(page_data, 'lxml')
        listing = parsed_html.body.find('div', attrs={'class': 'programListing'})
        rows = listing.find_all('div', attrs={'class': 'listingRow'})

        for row in rows:
            title = re.sub('<.*?>', '', row.find('div', attrs={'class': 'listingTitle'}).text.strip())
            date = re.sub('<.*?>', '', row.find('div', attrs={'class': 'listingDate'}).text.strip()).replace(':', '')
            data.append([title, date])

        return data
