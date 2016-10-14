import concurrent.futures
from typing import List

import flask
import flask_caching
from flask import Response

import epg
from channel import Channel
from channel_ids import CHANNEL_LIST, LBC_STREAM_FETCHER, JADEED_STREAM_FETCHER, EU, US

root = flask.Flask(__name__)
cache = flask_caching.Cache(root, config={'CACHE_TYPE': 'simple'})
app = root.wsgi_app


@root.route('/channels')
@root.route('/channels/eu')
def channels_route_default():
    return __get_channels_response_lines(flask.request.url_root, EU)


@root.route('/channels/us')
def channels_route_us():
    return __get_channels_response_lines(flask.request.url_root, US)


@root.route('/channel/' + LBC_STREAM_FETCHER.get_route_name())
@cache.cached(timeout=300)
def lbc_route():
    return __get_stream_lines(LBC_STREAM_FETCHER)


@root.route('/channel/' + JADEED_STREAM_FETCHER.get_route_name())
@cache.cached(timeout=120)
def jadeed_route():
    return __get_stream_lines(JADEED_STREAM_FETCHER)


@root.route('/epg')
@root.route('/epg/eu')
@cache.cached(timeout=3600)
def epg_route_default():
    return __get_epg_response(EU)


@root.route('/epg/us')
@cache.cached(timeout=3600)
def epg_route_us():
    return __get_epg_response(US)


def __filter_locations(channel_list: List[Channel], location: str) -> List[Channel]:
    return filter(lambda channel: channel.available_in(location), channel_list)


def __get_channels_response_lines(host: str, location: str) -> Response:
    response_list = ['#EXTM3U']
    filtered_channels = __filter_locations(CHANNEL_LIST, location)
    for channel in filtered_channels:
        if channel.stream_fetcher is not None:
            url = host + 'channel/' + channel.stream_fetcher.get_route_name()
        else:
            url = channel.url

        response_list.append('#EXTINF:-1 tvg-id="' + str(
            channel.channel_id) + '" tvg-logo="' + channel.logo + '", ' + channel.name + '\n' + url)

    return Response('\n'.join(response_list), mimetype='text/plain')


def __get_stream_lines(fetcher) -> Response:
    playlist = fetcher.fetch_stream_url()
    return flask.redirect(playlist, code=302)


def __get_epg_response(location: str) -> Response:
    response_string = '<?xml version="1.0" encoding="utf-8" ?>\n'
    response_string += '<!DOCTYPE tv SYSTEM "xmltv.dtd">\n'
    response_string += '<tv>'

    for channel in __filter_locations(CHANNEL_LIST, location):
        response_string += epg.get_channel(channel.channel_id, channel.name)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(epg.get_epg, channel): channel for channel in
                   __filter_locations(CHANNEL_LIST, location)}
        for future in concurrent.futures.as_completed(futures):
            response_string += future.result()

    response_string += '</tv>'

    return Response(response_string, mimetype='text/xml')
