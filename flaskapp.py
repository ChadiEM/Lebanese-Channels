import urllib
import urllib.error
import urllib.request
import xml.etree.ElementTree

import flask
import flask_cache

import epg
from channel_ids import *

flask_app = flask.Flask(__name__)
flask_app.register_blueprint(epg.epg_api)
cache = flask_cache.Cache(flask_app, config={'CACHE_TYPE': 'simple'})
app = flask_app.wsgi_app


@flask_app.route('/channels')
def get_channels():
    response = [generate_headers(),
                generate_channel(LBC_NAME, LBC_ID,
                                 'http://localhost:12589/channel/lbc',
                                 'http://www.lbcgroup.tv/programsimages/PCL-5-635531118011703749.png'),
                generate_channel(LBC_DRAMA_NAME, LBC_DRAMA_ID,
                                 'http://localhost:12589/channel/lbcdrama',
                                 'http://www.lbcgroup.tv/programsimages/Programs-Mp-668-635842240766782107.JPG'),
                generate_channel(MTV_NAME, MTV_ID,
                                 'http://livestreaming1.itworkscdn.net/mtvlive/smil:mtvmob.smil/playlist.m3u8',
                                 'http://mtv.com.lb/Content/images/mtv.jpg'),
                generate_channel(OTV_NAME, OTV_ID,
                                 'http://livestreaming.itworkscdn.net/otvmobile/otvlive_2/playlist.m3u8',
                                 'http://www.otv.com.lb/beta/images/logo.png'),
                generate_channel(JADEED_NAME, JADEED_ID,
                                 'http://localhost:12589/channel/jadeed',
                                 'http://www.aljadeed.tv/images/logo.png'),
                generate_channel(FUTURE_NAME, FUTURE_ID,
                                 'http://futuretv.cdn.mangomolo.com/futuretv/futuretv/playlist.m3u8',
                                 'http://www.futuretvnetwork.com/demo/wp-content/uploads/2014/05/goodnews-rtl.png'),
                generate_channel(NOURSAT_NAME, NOURSAT_ID,
                                 'rtsp://svs.itworkscdn.net/nour4satlive/livestream',
                                 'http://noursat.tv/images/main-logo.png'),
                generate_channel(NOURSAT_KODDASS_NAME, NOURSAT_KODDASS_ID,
                                 'rtsp://svs.itworkscdn.net/nour1satlive/livestream',
                                 'http://noursat.tv/mediafiles/channels/koddass-logo.png'),
                generate_channel(NOURSAT_SHARQ_NAME, NOURSAT_SHARQ_ID,
                                 'rtsp://svs.itworkscdn.net/nour8satlive/livestream',
                                 'http://noursat.tv/mediafiles/channels/sharq-logo.png')]

    return flask.Response('\n'.join(response), mimetype='text/plain')


def generate_headers():
    return '#EXTM3U'


def generate_channel(name, channel_id, url, logo):
    return '#EXTINF:-1 tvg-id="' + str(channel_id) + '" tvg-logo="' + logo + '", ' + name + '\n' + url


@flask_app.route('/channel/jadeed')
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


@flask_app.route('/channel/lbc')
@cache.cached(timeout=300)
def lbc():
    html = make_initial_request('http://mobilefeeds.lbcgroup.tv/getCategories.aspx')

    root = xml.etree.ElementTree.fromstring(html)
    playlist = root.find('watchLive').text
    html = make_request(playlist)

    return make_response(playlist, html)


@flask_app.route('/channel/lbcdrama')
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
