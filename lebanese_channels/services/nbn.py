from lebanese_channels.channel import Channel
from lebanese_channels.services.utils import stream


class NBN(Channel):
    def get_name(self) -> str:
        return 'NBN'

    def get_logo(self) -> str:
        return 'http://www.nbn.com.lb/wp-content/uploads/2017/02/nbnlogoforsite3.png'

    def get_stream_url(self) -> str:
        return stream.fetch_from('http://player.l1vetv.com/nbn')

    def get_epg_data(self):
        return None
