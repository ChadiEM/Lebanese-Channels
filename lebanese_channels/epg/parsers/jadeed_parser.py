import datetime
import re
from typing import Dict

import bs4

from lebanese_channels import utils
from lebanese_channels.epg import epg_utils
from lebanese_channels.epg.epg_parser import EPGParser
from lebanese_channels.epg.program_data import ProgramData


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
            hour = int(time_string_split[0])
            minute = int(time_string_split[1])

            links_div = row.find('div', attrs={'class': 'listingLink'})
            page_url_anchor = links_div.find_all('a')[1]
            program_id = page_url_anchor['href'].split('=')[1]

            start_time = datetime.datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
            program_data = ProgramData(title, start_time)
            data.append(program_data)

            additional_mappings[program_data] = 'http://aljadeed.tv/arabic/about-program?programid=' + program_id

        epg_utils.fill_end_times(data)
        fill_jadeed_additional_mappings(additional_mappings)

        return data


def fill_jadeed_additional_mappings(additional_mappings: Dict[ProgramData, str]):
    for program_data, url in additional_mappings.items():
        html = utils.get_response(url)
        parsed_html = bs4.BeautifulSoup(html, 'lxml')

        image_div = parsed_html.find('div', attrs={'class': 'mainArtistImage'})
        image_src = 'http://aljadeed.tv' + image_div.img['src'].replace(" ", "%20")
        program_data.icon = image_src

        text_div = parsed_html.find('div', attrs={'class': 'newsContent'})
        program_data.desc = text_div.text
