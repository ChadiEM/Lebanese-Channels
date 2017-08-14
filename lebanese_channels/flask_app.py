import concurrent.futures
from typing import List, Iterator

import flask
import flask_caching
from flask import Response

from lebanese_channels import epg
from lebanese_channels.channel import Channel
from lebanese_channels.channel_ids import CHANNEL_LIST, EU, US
from lebanese_channels.display_item import DisplayItem

root = flask.Flask(__name__)
cache = flask_caching.Cache(root, config={'CACHE_TYPE': 'simple'})
app = root.wsgi_app


@cache.cached(timeout=60)
def channel_stream():
    url_rule = flask.request.url_rule.rule
    target = url_rule.split('/channel/')[1]
    for current_channel in CHANNEL_LIST:
        if current_channel.stream_fetcher is not None and current_channel.stream_fetcher.get_route_name() == target:
            return __get_stream_lines(current_channel.stream_fetcher)


for channel in CHANNEL_LIST:
    if channel.stream_fetcher is not None:
        root.add_url_rule('/channel/' + channel.stream_fetcher.get_route_name(), view_func=channel_stream)


@root.route('/channels')
@root.route('/channels/eu')
def channels_route_default():
    return __get_channels_response_lines(flask.request.url_root, flask.request.args.get('format'), EU)


@root.route('/channels/us')
def channels_route_us():
    return __get_channels_response_lines(flask.request.url_root, flask.request.args.get('format'), US)


@root.route('/epg')
@root.route('/epg/eu')
@cache.cached(timeout=3600)
def epg_route_default():
    return __get_epg_response(EU)


@root.route('/epg/us')
@cache.cached(timeout=3600)
def epg_route_us():
    return __get_epg_response(US)


def __filter_locations(channel_list: List[Channel], location: str) -> Iterator[Channel]:
    return filter(lambda current_channel: current_channel.available_in(location), channel_list)


def __get_channels_response_lines(host: str, result_format: str, location: str) -> Response:
    display_items = []
    filtered_channels = __filter_locations(CHANNEL_LIST, location)
    for current_channel in filtered_channels:
        if current_channel.stream_fetcher is not None:
            url = host + 'channel/' + current_channel.stream_fetcher.get_route_name()
        else:
            url = current_channel.url

        display_items.append(DisplayItem(current_channel.channel_id, current_channel.name, url, current_channel.logo))

    if result_format is None or result_format == 'm3u8':
        response_list = ['#EXTM3U']
        for display_item in display_items:
            response_list.append('#EXTINF:-1'
                                 + ' tvg-id="' + str(display_item.channel_id) + '"'
                                 + ' tvg-logo="' + display_item.channel_logo + '"'
                                 + ', ' + display_item.channel_name
                                 + '\n'
                                 + display_item.channel_url)

        return Response('\n'.join(response_list), mimetype='application/vnd.apple.mpegurl')
    elif result_format == 'html':
        response_list = []

        response_list.append('<!DOCTYPE html>')
        response_list.append('<html>')

        response_list.append('<head>')
        response_list.append('<title>Channel List</title>')
        response_list.append('</head>')

        response_list.append('<body>')
        response_list.append('<ul>')

        for display_item in display_items:
            response_list.append(
                '<li><a href="' + display_item.channel_url + '">' + display_item.channel_name + '</a></li>')

        response_list.append('</ul>')
        response_list.append('</body>')
        response_list.append('</html>')
        return Response('\n'.join(response_list), mimetype='text/html')
    else:
        return Response('Unknown Format', mimetype='text/plain')


def __get_stream_lines(fetcher) -> Response:
    stream_lines_list = fetcher.fetch_stream_data()
    return Response('\n'.join(stream_lines_list), mimetype='application/vnd.apple.mpegurl')


def __get_epg_response(location: str) -> Response:
    response_string = '<?xml version="1.0" encoding="utf-8" ?>\n'
    response_string += '<!DOCTYPE tv SYSTEM "xmltv.dtd">\n'
    response_string += '<tv>'

    for current_channel in __filter_locations(CHANNEL_LIST, location):
        response_string += epg.get_channel(current_channel.channel_id, current_channel.name)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(epg.get_epg, current_channel): current_channel for current_channel in
                   __filter_locations(CHANNEL_LIST, location)}
        for future in concurrent.futures.as_completed(futures):
            response_string += future.result()

    response_string += '</tv>'

    return Response(response_string, mimetype='text/xml')
