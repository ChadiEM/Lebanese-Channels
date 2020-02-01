import logging

import flask
from flask import Response

from lebanese_channels.channel_ids import CHANNEL_LIST
from lebanese_channels.display_item import DisplayItem

app = flask.Flask(__name__)

logger = logging.getLogger(__name__)


@app.route('/channel/<name>')
def channel_route_default(name):
    return __channel_stream(name)


@app.route('/channels')
def channels_route_default():
    return __get_channels_response_lines(flask.request.url_root, flask.request.args.get('format'))


def __channel_stream(target):
    for channel in CHANNEL_LIST:
        if channel.get_route_name() == target:
            url = channel.get_stream_url()
            return flask.redirect(url, code=302)


def __get_channels_response_lines(host: str, result_format: str) -> Response:
    display_items = []

    for channel in CHANNEL_LIST:
        url = host + 'channel/' + channel.get_route_name()
        display_items.append(
            DisplayItem(channel.get_route_name(), channel.get_name(), url, channel.get_logo()))

    if result_format is None or result_format == 'm3u8':
        response_list = ['#EXTM3U']
        for display_item in display_items:
            response_list.append('#EXTINF:-1'
                                 + ' tvg-id="' + display_item.channel_short_name + '"'
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
