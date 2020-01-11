from lebanese_channels.channel import Channel
from lebanese_channels.utils import stream


class TeleLiban(Channel):
    def get_name(self) -> str:
        return 'Tele Liban'

    def get_logo(self) -> str:
        return 'http://www.teleliban.com.lb/images/telelogo.png'

    def get_stream_url(self) -> str:
        return stream.fetch_from('http://www.teleliban.com.lb/live')
