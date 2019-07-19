from lebanese_channels.channel import Channel
from lebanese_channels.utils import stream


class MTV(Channel):
    def get_name(self) -> str:
        return 'MTV'

    def get_logo(self) -> str:
        return 'http://mtv.com.lb/Content/images/logo-header.jpg'

    def get_stream_url(self) -> str:
        return stream.fetch_from('https://www.mtv.com.lb/Live/Player')
