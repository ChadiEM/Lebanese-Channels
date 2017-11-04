import itertools

from lebanese_channels.channel import Channel
from lebanese_channels.epg_data import LBCEPGData, MTVEPGData, JadeedEPGData, NoursatEPGData
from lebanese_channels.epg_parsers import LBCParser, MTVParser, JadeedParser, NoursatParser
from lebanese_channels.stream_fetcher import LBCStreamFetcher, GenericStreamFetcher

EU = 'eu'
US = 'us'
COUNTER = itertools.count(start=1)

LBC_NAME = 'LBC Europe'
LBC_STREAM_FETCHER = LBCStreamFetcher()
LBC_LOGO = 'http://www.lbcgroup.tv/programsimages/PCL-5-635531118011703749.png'
LBC_NOT_AVAILABLE_IN = [US]
LBC_EPG_DATA = LBCEPGData()
LBC_EPG_PARSER = LBCParser()

MTV_NAME = 'MTV'
MTV_STREAM_FETCHER = GenericStreamFetcher('mtv', 'http://mtv.com.lb/Live/Player')
MTV_LOGO = 'http://mtv.com.lb/Content/images/mtv.jpg'
MTV_NOT_AVAILABLE_IN = [US]
MTV_EPG_DATA = MTVEPGData()
MTV_EPG_PARSER = MTVParser()

OTV_NAME = 'OTV'
OTV_STREAM_FETCHER = GenericStreamFetcher('otv', 'http://www.otv.com.lb/new-live.php')
OTV_LOGO = 'http://www.otv.com.lb/beta/images/logo.png'

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
NBN_LOGO = 'http://www.nbn.com.lb/wp-content/uploads/2016/09/nbn-logo-normal-2.png'

MANAR_NAME = 'Al Manar'
MANAR_STREAM_URL = 'http://edge.mediaforall.net:1935/liveorigin/livestream_480p/playlist.m3u8'
MANAR_LOGO = 'http://english.almanar.com.lb/framework/assets/images/logo-tech.png'

NOURSAT_NAME = 'Noursat'
NOURSAT_STREAM_URL = 'rtsp://svs.itworkscdn.net/nour4satlive/livestream'
NOURSAT_LOGO = 'http://noursat.tv/images/main-logo.png'
NOURSAT_EPG_DATA = NoursatEPGData()
NOURSAT_EPG_PARSER = NoursatParser()

NOURSAT_KODDASS_NAME = 'Nour Al Koddass'
NOURSAT_KODDASS_STREAM_URL = 'rtsp://svs.itworkscdn.net/nour1satlive/livestream'
NOURSAT_KODDASS_LOGO = 'http://noursat.tv/mediafiles/channels/koddass-logo.png'

NOURSAT_SHARQ_NAME = 'Nour Sharq'
NOURSAT_SHARQ_STREAM_URL = 'rtsp://svs.itworkscdn.net/nour8satlive/livestream'
NOURSAT_SHARQ_LOGO = 'http://noursat.tv/mediafiles/channels/sharq-logo.png'

LBC_SPORTS_NAME = 'LBC Sports'
LBC_SPORTS_STREAM_FETCHER = GenericStreamFetcher('lbc_sports', 'https://www.lbcgroup.tv/sports')
LBC_SPORTS_LOGO = 'http://www.lbcgroup.tv/programsimages/PCL-5-635531118011703749.png'

CHANNEL_LIST = [
    Channel(next(COUNTER), LBC_NAME, LBC_LOGO, stream_fetcher=LBC_STREAM_FETCHER, not_available_in=LBC_NOT_AVAILABLE_IN,
            epg_data=LBC_EPG_DATA,
            epg_parser=LBC_EPG_PARSER),
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
    Channel(next(COUNTER), NOURSAT_KODDASS_NAME, NOURSAT_KODDASS_LOGO, stream_url=NOURSAT_KODDASS_STREAM_URL),
    Channel(next(COUNTER), NOURSAT_SHARQ_NAME, NOURSAT_SHARQ_LOGO, stream_url=NOURSAT_SHARQ_STREAM_URL),
    Channel(next(COUNTER), LBC_SPORTS_NAME, LBC_SPORTS_LOGO, stream_fetcher=LBC_SPORTS_STREAM_FETCHER)
]
