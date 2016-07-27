import abc
import re
import json
import datetime
import urllib
import urllib.request
import urllib.error
import bs4
import flask

epg_api = flask.Blueprint('epg_api', __name__)


@epg_api.route('/epg')
def epg():
    response = """<?xml version="1.0" encoding="utf-8" ?>
<tv>
<channel id="1">
<display-name lang="en">LBC Europe</display-name>
</channel>
<channel id="2">
<display-name lang="en">MTV</display-name>
</channel>
<channel id="3">
<display-name lang="en">OTV</display-name>
</channel>
<channel id="4">
<display-name lang="en">Aljadeed</display-name>
</channel>
"""

    response += get_epg(
        'http://www.lbcgroup.tv/schedule-channels-date/5/' + datetime.datetime.now().strftime("%Y/%m/%d") + '/ar',
        LBCParser(), 100, '1')
    response += get_epg('http://mtv.com.lb/program/getDayGridByDayName?dayName=', MTVParser(), -100, '2')
    response += get_epg(
        'http://www.otv.com.lb/beta/_ajax.php?action=grid&id=' + str(datetime.datetime.today().weekday() + 1) + '&r=14',
        OTVParser(), -100, '3')
    response += get_epg('http://www.aljadeed.tv/arabic/programs/schedule', JadeedParser(), -100, '4')

    response += "</tv>"
    return flask.Response(response, mimetype='text/xml')


def get_epg(url, parser, shift, chanid):
    try:
        html = make_schedule_request(url)
        data = parser.parse(html)
        start_end_data = process_data(data, shift)
        return get_response(start_end_data, chanid)
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
    today = datetime.datetime.now().strftime("%Y%m%d")
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y%m%d")

    index = 0
    for data_row in data:
        start_time = str(int(data_row[1]) + shift).zfill(4)
        if index + 1 >= len(data):
            end_datetime = tomorrow + "000000"
        else:
            end_datetime = today + str(int(data[index + 1][1]) + shift).zfill(4)

        if int(start_time) >= 0:
            start = today + start_time + "00 +0100"
            end = end_datetime + "00 +0100"
            title = data_row[0]
            processed_data.append([start, end, title])
        index += 1

    return processed_data


def get_response(start_end_data, chanid):
    response = ''

    for pdata in start_end_data:
        response += "<programme start=\"" + pdata[0] + "\" stop=\"" + pdata[1] + "\" channel=\"" + chanid + "\">"
        response += "<title lang=\"en\">" + pdata[2] + "</title>"
        response += "</programme>"

    return response


class Parser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse(self, page_data):
        return


class LBCParser(Parser):
    def parse(self, page_data):
        data = []
        parsed_html = bs4.BeautifulSoup(page_data, 'lxml')

        listings = parsed_html.find_all('table', attrs={'class': 'ScheduleMoreThan452'})

        for listing in listings:
            title = listing.find('h2').find('a').text.strip()
            date = listing.find('span', attrs={'class': 'FromTimeSchedule'}).text.replace(':', '')

            data.append([title, date])

        return data


class MTVParser(Parser):
    def parse(self, page_data):
        data = []

        json_parsed = json.loads(page_data)

        for program in json_parsed[0]['programs']:
            name = program['programName']
            time = program['time'].replace(':', '')
            data.append([name, time])

        return data


class OTVParser(Parser):
    def parse(self, page_data):
        data = []
        parsed_html = bs4.BeautifulSoup(page_data, 'lxml')
        listings = parsed_html.find_all('li')

        for listing in listings:
            title = listing.find('div', attrs={'class': 'b2'}).find('h3').text
            date = listing.find('div', attrs={'class': 'b3'}).find('span').text.split()[0].replace(':', '')

            data.append([title, date])

        return data


class JadeedParser(Parser):
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
