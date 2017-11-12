import itertools

from lebanese_channels.channel import Channel
from lebanese_channels.epg.data.jadeed_data import JadeedEPGData
from lebanese_channels.epg.data.lb2_data import LB2EPGData
from lebanese_channels.epg.data.lbc_data import LBCEPGData
from lebanese_channels.epg.data.mtv_data import MTVEPGData
from lebanese_channels.epg.data.noursat_data import NoursatEPGData
from lebanese_channels.epg.parsers.jadeed_parser import JadeedParser
from lebanese_channels.epg.parsers.lbc_parser import LBCParser
from lebanese_channels.epg.parsers.mtv_parser import MTVParser
from lebanese_channels.epg.parsers.noursat_parser import NoursatParser
from lebanese_channels.stream.fetchers.generic_fetcher import GenericStreamFetcher
from lebanese_channels.stream.fetchers.lbc_fetcher import LBCStreamFetcher

EU = 'eu'
US = 'us'
COUNTER = itertools.count(start=1)

LBC_NAME = 'LBC Europe'
LBC_STREAM_FETCHER = LBCStreamFetcher()
LBC_LOGO = 'http://www.lbcgroup.tv/programsimages/PCL-5-635531118011703749.png'
LBC_NOT_AVAILABLE_IN = [US]
LBC_EPG_DATA = LBCEPGData()
LBC_EPG_PARSER = LBCParser()

LB2_NAME = 'LB2'
LB2_STREAM_URL = 'https://svs.itworkscdn.net/lbcdramalive/drama/playlist.m3u8'
LB2_LOGO = 'https://pbs.twimg.com/profile_images/776806340790476800/CMdKBI7R_400x400.jpg'
LB2_EPG_DATA = LB2EPGData()
LB2_EPG_PARSER = LBCParser()

MTV_NAME = 'MTV'
MTV_STREAM_FETCHER = GenericStreamFetcher('mtv', 'http://mtv.com.lb/Live/Player')
MTV_LOGO = 'http://mtv.com.lb/Content/images/mtv.jpg'
MTV_NOT_AVAILABLE_IN = [US]
MTV_EPG_DATA = MTVEPGData()
MTV_EPG_PARSER = MTVParser()

OTV_NAME = 'OTV'
OTV_STREAM_FETCHER = GenericStreamFetcher('otv', 'http://www.otv.com.lb/new-live.php')
OTV_LOGO = 'https://lh3.googleusercontent.com/7faSyx5uV7BjRXzn6hcbTPs8sfY0WlreUI7XZZei-u7VJTNpU7LVnTA7c7euazfbcso=w300'

JADEED_NAME = 'Aljadeed'
JADEED_STREAM_FETCHER = GenericStreamFetcher('jadeed', 'http://player.l1vetv.com/aljadeed/index-1.php')
JADEED_LOGO = 'http://www.aljadeed.tv/images/logo.png'
JADEED_EPG_DATA = JadeedEPGData()
JADEED_EPG_PARSER = JadeedParser()

FUTURE_NAME = 'Future TV'
FUTURE_STREAM_URL = 'http://futuretv.cdn.mangomolo.com/futuretv/futuretv/playlist.m3u8'
FUTURE_LOGO = 'http://www.futuretvnetwork.com/demo/wp-content/uploads/2014/05/goodnews-rtl.png'

NBN_NAME = 'NBN'
NBN_STREAM_FETCHER = GenericStreamFetcher('nbn', 'http://player.l1vetv.com/nbn')
NBN_LOGO = 'http://www.nbn.com.lb/wp-content/uploads/2017/02/nbnlogoforsite3.png'

MANAR_NAME = 'Al Manar'
MANAR_STREAM_URL = 'http://live2.mediaforall.net:1935/liveorigin/livestream_480p/playlist.m3u8'
MANAR_LOGO = 'http://english.almanar.com.lb/framework/assets/images/logo-tech.png'

NOURSAT_NAME = 'Noursat'
NOURSAT_STREAM_URL = 'https://svs.itworkscdn.net/nour4satlive/livestream/playlist.m3u8'
NOURSAT_LOGO = 'http://noursat.tv/images/main-logo.png'
NOURSAT_EPG_DATA = NoursatEPGData()
NOURSAT_EPG_PARSER = NoursatParser()

LBC_SPORTS_NAME = 'LBC Sports'
LBC_SPORTS_STREAM_FETCHER = GenericStreamFetcher('lbc_sports', 'https://www.lbcgroup.tv/sports')
LBC_SPORTS_LOGO = 'http://www.lbcgroup.tv/programsimages/PCL-5-635531118011703749.png'

CHANNEL_LIST = [
    Channel(next(COUNTER), LBC_NAME, LBC_LOGO, stream_fetcher=LBC_STREAM_FETCHER, not_available_in=LBC_NOT_AVAILABLE_IN,
            epg_data=LBC_EPG_DATA,
            epg_parser=LBC_EPG_PARSER),
    Channel(next(COUNTER), LB2_NAME, LB2_LOGO, stream_url=LB2_STREAM_URL,
            epg_data=LB2_EPG_DATA,
            epg_parser=LB2_EPG_PARSER),
    Channel(next(COUNTER), MTV_NAME, MTV_LOGO, stream_fetcher=MTV_STREAM_FETCHER, not_available_in=MTV_NOT_AVAILABLE_IN,
            epg_data=MTV_EPG_DATA,
            epg_parser=MTV_EPG_PARSER),
    Channel(next(COUNTER), OTV_NAME, OTV_LOGO, stream_fetcher=OTV_STREAM_FETCHER),
    Channel(next(COUNTER), JADEED_NAME, JADEED_LOGO, stream_fetcher=JADEED_STREAM_FETCHER,
            epg_data=JADEED_EPG_DATA,
            epg_parser=JADEED_EPG_PARSER),
    Channel(next(COUNTER), NBN_NAME, NBN_LOGO, stream_fetcher=NBN_STREAM_FETCHER),
    Channel(next(COUNTER), FUTURE_NAME, FUTURE_LOGO, stream_url=FUTURE_STREAM_URL),
    Channel(next(COUNTER), MANAR_NAME, MANAR_LOGO, stream_url=MANAR_STREAM_URL),
    Channel(next(COUNTER), NOURSAT_NAME, NOURSAT_LOGO, stream_url=NOURSAT_STREAM_URL,
            epg_data=NOURSAT_EPG_DATA,
            epg_parser=NOURSAT_EPG_PARSER),
    Channel(next(COUNTER), LBC_SPORTS_NAME, LBC_SPORTS_LOGO, stream_fetcher=LBC_SPORTS_STREAM_FETCHER)
]
