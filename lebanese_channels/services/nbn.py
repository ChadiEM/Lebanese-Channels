from lebanese_channels.channel import Channel
from lebanese_channels.utils import stream


class NBN(Channel):
    def get_name(self) -> str:
        return 'NBN'

    def get_logo(self) -> str:
        return 'https://nbntv.me/wp-content/uploads/2018/08/cropped-nbn-logo-512-192x192.jpg'

    def get_stream_url(self) -> str:
        return stream.fetch_from('http://player.l1vetv.com/nbn')
