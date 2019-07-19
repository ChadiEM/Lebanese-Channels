from lebanese_channels.channel import Channel


class Noursat(Channel):
    def get_name(self) -> str:
        return 'Noursat'

    def get_logo(self) -> str:
        return 'http://noursat.tv/images/main-logo.png'

    def get_stream_url(self) -> str:
        return 'https://svs.itworkscdn.net/nour4satlive/livestream/playlist.m3u8'
