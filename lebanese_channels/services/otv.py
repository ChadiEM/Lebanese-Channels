from lebanese_channels.channel import Channel
from lebanese_channels.services.utils import stream


class OTV(Channel):
    def get_name(self) -> str:
        return 'OTV'

    def get_logo(self) -> str:
        return 'https://lh3.googleusercontent.com/7faSyx5uV7BjRXzn6hcbTPs8sfY0WlreUI7XZZei-u7VJTNpU7LVnTA7c7euazfbcso' \
               '=w300 '

    def get_stream_url(self) -> str:
        return stream.fetch_from('http://www.otv.com.lb/new-live.php')

    def get_epg_data(self):
        return None
