from lebanese_channels.channel import Channel


class OTV(Channel):
    def get_name(self) -> str:
        return 'OTV'

    def get_logo(self) -> str:
        return 'https://lh3.googleusercontent.com/7faSyx5uV7BjRXzn6hcbTPs8sfY0WlreUI7XZZei-u7VJTNpU7LVnTA7c7euazfbcso' \
               '=w300 '

    def get_stream_url(self) -> str:
        return 'https://svs.itworkscdn.net/otvlebanonlive/otv.smil/playlist.m3u8'

    def get_epg_data(self):
        return None
