import concurrent.futures
import urllib
import urllib.error
import urllib.request
from xml.sax.saxutils import escape

import flask

from channel_ids import *

epg_api = flask.Blueprint('epg_api', __name__)


@epg_api.route('/epg')
def epg():
    response = '<?xml version="1.0" encoding="utf-8" ?>\n'
    response += '<!DOCTYPE tv SYSTEM "xmltv.dtd">\n'
    response += '<tv>'

    for channel in CHANNEL_LIST:
        response += get_channel(channel.get_channel_id(), channel.get_name())

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(get_epg, channel): channel for channel in CHANNEL_LIST}
        for future in concurrent.futures.as_completed(futures):
            response += future.result()

    response += '</tv>'
    return flask.Response(response, mimetype='text/xml')


def get_channel(channel_id, channel_name):
    return '<channel id="' + str(channel_id) + '"><display-name lang="en">' + channel_name + '</display-name></channel>'


def get_epg(channel):
    if channel.get_epg_data() is None or channel.get_epg_parser() is None:
        return ''

    urls = channel.get_epg_data().get_fetch_url()

    if isinstance(urls, list):
        response = ''
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(fetch_epg, channel, url): url for url in urls}
            for future in concurrent.futures.as_completed(futures):
                response += future.result()
    else:
        response = fetch_epg(channel, urls)

    return response


def fetch_epg(channel, url):
    try:
        html = make_schedule_request(url)
        start_end_data = channel.get_epg_parser().parse(html)
        return get_response(start_end_data, channel.get_channel_id())
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


def get_response(program_datas, channel_id):
    response = ''

    for program_data in program_datas:
        response += '<programme start="' + date_to_string(program_data.get_start_time()) + '" stop="' + date_to_string(
            program_data.get_stop_time()) + '" channel="' + str(channel_id) + '">'
        response += '<title lang="en">' + program_data.get_name() + '</title>'
        if program_data.get_desc() is not None:
            response += '<desc lang="en">' + program_data.get_desc() + '</desc>'
        if program_data.get_category() is not None:
            response += '<category lang="en">' + escape(program_data.get_category()) + '</category>'
        response += '</programme>'

    return response


def date_to_string(date):
    return date.strftime("%Y%m%d %H%M00 +0100")
