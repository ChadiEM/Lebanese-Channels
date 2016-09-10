import abc
import datetime
import json
import re
import urllib
import urllib.error
import urllib.request

import bs4
import flask

from channel_ids import *

epg_api = flask.Blueprint('epg_api', __name__)


@epg_api.route('/epg')
def epg():
    response = '<?xml version="1.0" encoding="utf-8" ?>'
    response += '<tv>'

    response += get_channel(LBC_NAME, LBC_ID)
    response += get_channel(LBC_DRAMA_NAME, LBC_DRAMA_ID)
    response += get_channel(MTV_NAME, MTV_ID)
    response += get_channel(OTV_NAME, OTV_ID)
    response += get_channel(JADEED_NAME, JADEED_ID)
    response += get_channel(FUTURE_NAME, FUTURE_ID)
    response += get_channel(NOURSAT_NAME, NOURSAT_ID)
    response += get_channel(NOURSAT_KODDASS_NAME, NOURSAT_KODDASS_ID)
    response += get_channel(NOURSAT_SHARQ_NAME, NOURSAT_SHARQ_ID)

    response += get_epg(
        'http://www.lbcgroup.tv/schedule-channels-date/5/' + datetime.datetime.now().strftime('%Y/%m/%d') + '/ar',
        LBCParser(), 100, LBC_ID)
    response += get_epg(
        'http://www.lbcgroup.tv/schedule-channels-date/6/' + datetime.datetime.now().strftime('%Y/%m/%d') + '/ar',
        LBCParser(), 0, LBC_DRAMA_ID)
    response += get_epg(
        'http://mtv.com.lb/program/getDayGridByDayName?dayName=',
        MTVParser(), -100, MTV_ID)
    response += get_epg(
        'http://www.otv.com.lb/beta/_ajax.php?action=grid&id=' + str(datetime.datetime.today().weekday() + 1) + '&r=14',
        OTVParser(), -100, OTV_ID)
    response += get_epg(
        'http://www.aljadeed.tv/arabic/programs/schedule',
        JadeedParser(), -100, JADEED_ID)

    response += '</tv>'
    return flask.Response(response, mimetype='text/xml')


def get_channel(name, channel_id):
    return '<channel id="' + str(channel_id) + '"><display-name lang="en">' + name + '</display-name></channel>'


def get_epg(url, parser, shift, channel_id):
    try:
        html = make_schedule_request(url)
        data = parser.parse(html)
        start_end_data = process_data(data, shift)
        return get_response(start_end_data, channel_id)
    except urllib.error.URLError:
        return ''


def make_schedule_request(url):
    req = urllib.request.Request(url)
    req.add_header('Accept', 'text/html')
    req.add_header('User-Agent',
                   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0')
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    response.close()
    return html


def process_data(data, shift):
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


def get_response(start_end_data, channel_id):
    response = ''

    for pdata in start_end_data:
        response += '<programme start="' + pdata[0] + '" stop="' + pdata[1] + '" channel="' + str(channel_id) + '">'
        response += '<title lang="en">' + pdata[2] + '</title>'
        response += '</programme>'

    return response


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
