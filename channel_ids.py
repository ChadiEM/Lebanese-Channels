import itertools

from channel import Channel
from epg_data import LBCEPGData, MTVEPGData, OTVEPGData, JadeedEPGData
from epg_parsers import LBCParser, MTVParser, OTVParser, JadeedParser
from stream_fetcher import LBCStreamFetcher, JadeedStreamFetcher

EU = 'eu'
US = 'us'
counter = itertools.count(start=1)

LBC_NAME = 'LBC Europe'
LBC_STREAM_FETCHER = LBCStreamFetcher()
LBC_LOGO = 'http://www.lbcgroup.tv/programsimages/PCL-5-635531118011703749.png'
LBC_NOT_AVAILABLE_IN = [US]
LBC_EPG_DATA = LBCEPGData()
LBC_EPG_PARSER = LBCParser()

MTV_NAME = 'MTV'
MTV_STREAM_URL = 'http://livestreaming1.itworkscdn.net/mtvlive/smil:mtvmob.smil/playlist.m3u8'
MTV_LOGO = 'http://mtv.com.lb/Content/images/mtv.jpg'
MTV_NOT_AVAILABLE_IN = [US]
MTV_EPG_DATA = MTVEPGData()
MTV_EPG_PARSER = MTVParser()

OTV_NAME = 'OTV'
OTV_STREAM_URL = 'http://livestreaming.itworkscdn.net/otvmobile/otvlive_2/playlist.m3u8'
OTV_LOGO = 'http://www.otv.com.lb/beta/images/logo.png'
OTV_EPG_DATA = OTVEPGData()
OTV_EPG_PARSER = OTVParser()

JADEED_NAME = 'Aljadeed'
JADEED_STREAM_FETCHER = JadeedStreamFetcher()
JADEED_LOGO = 'http://www.aljadeed.tv/images/logo.png'
JADEED_EPG_DATA = JadeedEPGData()
JADEED_EPG_PARSER = JadeedParser()

FUTURE_NAME = 'Future TV'
FUTURE_STREAM_URL = 'http://futuretv.cdn.mangomolo.com/futuretv/futuretv/playlist.m3u8'
FUTURE_LOGO = 'http://www.futuretvnetwork.com/demo/wp-content/uploads/2014/05/goodnews-rtl.png'

MANAR_NAME = 'Al Manar'
MANAR_STREAM_URL = 'http://edge.mediaforall.net:1935/liveorigin/livestream_480p/playlist.m3u8'
MANAR_LOGO = 'http://english.almanar.com.lb/framework/assets/images/logo-tech.png'

NOURSAT_NAME = 'Noursat'
NOURSAT_STREAM_URL = 'rtsp://svs.itworkscdn.net/nour4satlive/livestream'
NOURSAT_LOGO = 'http://noursat.tv/images/main-logo.png'

NOURSAT_KODDASS_NAME = 'Nour Al Koddass'
NOURSAT_KODDASS_STREAM_URL = 'rtsp://svs.itworkscdn.net/nour1satlive/livestream'
NOURSAT_KODDASS_LOGO = 'http://noursat.tv/mediafiles/channels/koddass-logo.png'

NOURSAT_SHARQ_NAME = 'Nour Sharq'
NOURSAT_SHARQ_STREAM_URL = 'rtsp://svs.itworkscdn.net/nour8satlive/livestream'
NOURSAT_SHARQ_LOGO = 'http://noursat.tv/mediafiles/channels/sharq-logo.png'

CHANNEL_LIST = [
    Channel(next(counter), LBC_NAME, LBC_LOGO, stream_fetcher=LBC_STREAM_FETCHER, not_available_in=LBC_NOT_AVAILABLE_IN,
            epg_data=LBC_EPG_DATA,
            epg_parser=LBC_EPG_PARSER),
    Channel(next(counter), MTV_NAME, MTV_LOGO, stream_url=MTV_STREAM_URL, not_available_in=MTV_NOT_AVAILABLE_IN,
            epg_data=MTV_EPG_DATA,
            epg_parser=MTV_EPG_PARSER),
    Channel(next(counter), OTV_NAME, OTV_LOGO, stream_url=OTV_STREAM_URL, epg_data=OTV_EPG_DATA,
            epg_parser=OTV_EPG_PARSER),
    Channel(next(counter), JADEED_NAME, JADEED_LOGO, stream_fetcher=JADEED_STREAM_FETCHER, epg_data=JADEED_EPG_DATA,
            epg_parser=JADEED_EPG_PARSER),
    Channel(next(counter), FUTURE_NAME, FUTURE_LOGO, stream_url=FUTURE_STREAM_URL),
    Channel(next(counter), MANAR_NAME, MANAR_LOGO, stream_url=MANAR_STREAM_URL),
    Channel(next(counter), NOURSAT_NAME, NOURSAT_LOGO, stream_url=NOURSAT_STREAM_URL),
    Channel(next(counter), NOURSAT_KODDASS_NAME, NOURSAT_KODDASS_LOGO, stream_url=NOURSAT_KODDASS_STREAM_URL),
    Channel(next(counter), NOURSAT_SHARQ_NAME, NOURSAT_SHARQ_LOGO, stream_url=NOURSAT_SHARQ_STREAM_URL),
]
