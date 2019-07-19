from lebanese_channels.channel import Channel


class Manar(Channel):
    def get_name(self) -> str:
        return 'Al Manar'

    def get_logo(self) -> str:
        return 'http://english.almanar.com.lb/framework/assets/images/logo-tech.png'

    def get_stream_url(self) -> str:
        return 'http://live2.mediaforall.net:1935/liveorigin/livestream_480p/playlist.m3u8'
