import xml.etree.ElementTree
import urllib
import urllib.error
import urllib.request

import itertools

import epg
import flask
import flask_cache

flask_app = flask.Flask(__name__)
flask_app.register_blueprint(epg.epg_api)
cache = flask_cache.Cache(flask_app, config={'CACHE_TYPE': 'simple'})
app = flask_app.wsgi_app


@flask_app.route('/channels')
def get_channels():
    channel_list = []
    counter = itertools.count(start=1)

    channel_list.append(
        generate_headers())
    channel_list.append(
        generate_channel("LBC Europe", counter, "http://localhost:12589/channel/lbc",
                         "http://www.lbcgroup.tv/programsimages/PCL-5-635531118011703749.png"))
    channel_list.append(
        generate_channel("LBC Drama", counter, "http://localhost:12589/channel/lbcdrama",
                         "http://www.lbcgroup.tv/programsimages/Programs-Mp-668-635842240766782107.JPG"))
    channel_list.append(
        generate_channel("MTV", counter, "http://livestreaming1.itworkscdn.net/mtvlive/smil:mtvmob.smil/playlist.m3u8",
                         "http://mtv.com.lb/Content/images/mtv.jpg"))
    channel_list.append(
        generate_channel("OTV", counter, "http://livestreaming.itworkscdn.net/otvmobile/otvlive_2/playlist.m3u8",
                         "http://www.otv.com.lb/beta/images/logo.png"))
    channel_list.append(
        generate_channel("Aljadeed", counter, "http://localhost:12589/channel/jadeed",
                         "http://www.aljadeed.tv/images/logo.png"))
    channel_list.append(
        generate_channel("Future TV", counter, "http://futuretv.cdn.mangomolo.com/futuretv/futuretv/playlist.m3u8",
                         "http://www.futuretvnetwork.com/demo/wp-content/uploads/2014/05/goodnews-rtl.png"))
    channel_list.append(
        generate_channel("Noursat", counter, "rtsp://svs.itworkscdn.net/nour4satlive/livestream",
                         "http://noursat.tv/images/main-logo.png"))
    channel_list.append(
        generate_channel("Nour Al Koddass", counter, "rtsp://svs.itworkscdn.net/nour1satlive/livestream",
                         "http://noursat.tv/mediafiles/channels/koddass-logo.png"))
    channel_list.append(
        generate_channel("Nour Sharq", counter, "rtsp://svs.itworkscdn.net/nour8satlive/livestream",
                         "http://noursat.tv/mediafiles/channels/sharq-logo.png"))

    return flask.Response('\n'.join(channel_list), mimetype='text/plain')


def generate_headers():
    return '#EXTM3U'


def generate_channel(name, counter, url, logo):
    return '#EXTINF:-1 tvg-id="' + str(next(counter)) + '" tvg-logo="' + logo + '", ' + name + '\n' + url


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
