from lebanese_channels.channel import Channel
from lebanese_channels.utils import stream


class Jadeed(Channel):
    def get_name(self) -> str:
        return 'Al Jadeed'

    def get_logo(self) -> str:
        return 'http://www.aljadeed.tv/images/logo.png'

    def get_stream_url(self) -> str:
        return stream.fetch_from('https://www.aljadeed.tv/arabic/live')
