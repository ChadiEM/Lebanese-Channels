from lebanese_channels.channel import Channel
from lebanese_channels.services.utils import stream


class LBCSports(Channel):
    def get_name(self) -> str:
        return 'LBC Sports'

    def get_logo(self) -> str:
        return 'http://www.lbcgroup.tv/programsimages/PCL-5-635531118011703749.png'

    def get_stream_url(self) -> str:
        return stream.fetch_from('https://www.lbcgroup.tv/sports')

    def get_epg_data(self):
        return None
