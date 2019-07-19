from lebanese_channels.channel import Channel


class Future(Channel):
    def get_name(self) -> str:
        return 'Future TV'

    def get_logo(self) -> str:
        return 'http://www.futuretvnetwork.com/images/logo-n2.png'

    def get_stream_url(self) -> str:
        return 'http://futuretv.cdn.mangomolo.com/futuretv/futuretv/playlist.m3u8'
