import urllib
import urllib.error
import urllib.request

import flask

from channel_ids import *

epg_api = flask.Blueprint('epg_api', __name__)


@epg_api.route('/epg')
def epg():
    response = '<?xml version="1.0" encoding="utf-8" ?>'
    response += '<tv>'

    for channel in CHANNEL_LIST:
        response += get_channel(channel.get_channel_id(), channel.get_name())

    for channel in CHANNEL_LIST:
        if channel.get_epg_data() is not None and channel.get_epg_parser() is not None:
            response += get_epg(channel.get_channel_id(), channel.get_epg_data().get_fetch_url(),
                                channel.get_epg_parser(), channel.get_epg_data().get_time_shift())

    response += '</tv>'
    return flask.Response(response, mimetype='text/xml')


def get_channel(channel_id, channel_name):
    return '<channel id="' + str(channel_id) + '"><display-name lang="en">' + channel_name + '</display-name></channel>'


def get_epg(channel_id, url, parser, shift):
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
