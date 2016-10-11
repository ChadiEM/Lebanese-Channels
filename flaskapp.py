import concurrent.futures

import flask
import flask_caching

import epg
from channel_ids import CHANNEL_LIST, LBC_STREAM_FETCHER, JADEED_STREAM_FETCHER

root = flask.Flask(__name__)
cache = flask_caching.Cache(root, config={'CACHE_TYPE': 'simple'})
app = root.wsgi_app


@root.route('/channels')
def channels_route():
    response_lines = __get_channels_response_lines(flask.request.url_root)
    return flask.Response('\n'.join(response_lines), mimetype='text/plain')


@root.route('/channel/' + LBC_STREAM_FETCHER.get_route_name())
@cache.cached(timeout=300)
def lbc_route():
    stream_lines = LBC_STREAM_FETCHER.fetch_stream_data()
    return flask.Response('\n'.join(stream_lines), mimetype='text/plain')


@root.route('/channel/' + JADEED_STREAM_FETCHER.get_route_name())
@cache.cached(timeout=120)
def jadeed_route():
    stream_lines = JADEED_STREAM_FETCHER.fetch_stream_data()
    return flask.Response('\n'.join(stream_lines), mimetype='text/plain')


@root.route('/epg')
@cache.cached(timeout=3600)
def epg_route():
    response = __get_epg_response()
    return flask.Response(response, mimetype='text/xml')


def __get_channels_response_lines(host):
    response = ['#EXTM3U']
    for channel in CHANNEL_LIST:
        if channel.stream_fetcher is not None:
            url = host + 'channel/' + channel.stream_fetcher.get_route_name()
        else:
            url = channel.url

        response.append('#EXTINF:-1 tvg-id="' + str(
            channel.channel_id) + '" tvg-logo="' + channel.logo + '", ' + channel.name + '\n' + url)
    return response


def __get_epg_response():
    response = '<?xml version="1.0" encoding="utf-8" ?>\n'
    response += '<!DOCTYPE tv SYSTEM "xmltv.dtd">\n'
    response += '<tv>'
    for channel in CHANNEL_LIST:
        response += epg.get_channel(channel.channel_id, channel.name)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(epg.get_epg, channel): channel for channel in CHANNEL_LIST}
        for future in concurrent.futures.as_completed(futures):
            response += future.result()
    response += '</tv>'
    return response
