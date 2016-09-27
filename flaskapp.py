import urllib
import urllib.error
import urllib.request
import xml.etree.ElementTree

import flask
import flask_caching

import epg
from channel_ids import *

channels = flask.Flask(__name__)
channels.register_blueprint(epg.epg_api)
cache = flask_caching.Cache(channels, config={'CACHE_TYPE': 'simple'})
app = channels.wsgi_app


@channels.route('/channels')
def get_channels():
    host = flask.request.url_root

    response = [generate_headers()]

    for channel in CHANNEL_LIST:
        if channel.get_route() is not None:
            url = host + 'channel/' + channel.get_route()
        else:
            url = channel.get_url()

        response.append(generate_channel(channel.get_name(), channel.get_channel_id(), url, channel.get_logo()))

    return flask.Response('\n'.join(response), mimetype='text/plain')


def generate_headers():
    return '#EXTM3U'


def generate_channel(name, channel_id, url, logo):
    return '#EXTINF:-1 tvg-id="' + str(channel_id) + '" tvg-logo="' + logo + '", ' + name + '\n' + url


@channels.route('/channel/jadeed')
@cache.cached(timeout=120)
def jadeed():
    html = make_initial_request('http://player.l1vetv.com/aljadeed/index-1.php')

    playlist = ''
    for line in html.splitlines():
        if 'file' in line and 'm3u8' in line:
            line_splitted = line.split('"')
            playlist = line_splitted[1]

    html = make_request(playlist)

    return make_response(playlist, html)


@channels.route('/channel/lbc')
@cache.cached(timeout=300)
def lbc():
    html = make_initial_request('http://mobilefeeds.lbcgroup.tv/getCategories.aspx')

    root = xml.etree.ElementTree.fromstring(html)
    playlist = root.find('watchLive').text
    html = make_request(playlist)

    return make_response(playlist, html)


@channels.route('/channel/lbc2')
@cache.cached(timeout=300)
def lbc_drama():
    playlist = 'https://svs.itworkscdn.net/lbcdramalive/drama/playlist.m3u8'
    html = make_request(playlist)

    return make_response(playlist, html)


def make_initial_request(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    response.close()
    return html


def make_request(playlist):
    req = urllib.request.Request(playlist)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Language', 'en-US,en;q=0.5')
    req.add_header('Accept-Encoding', 'gzip, deflate')
    req.add_header('Connection', 'close')
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')

    response.close()

    return html


def make_response(playlist, html):
    list_response = []
    start_index = playlist.find('.m3u8')
    if start_index != -1:
        while playlist[start_index] != '/' and start_index > 0:
            start_index -= 1

    prefix = playlist[:start_index + 1]

    for line in html.splitlines():
        if not line.startswith('#'):
            list_response.append(prefix + line)
        else:
            list_response.append(line)

    return flask.Response('\n'.join(list_response), mimetype='text/plain')
