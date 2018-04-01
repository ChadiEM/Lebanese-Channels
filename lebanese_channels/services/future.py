from lebanese_channels.channel import Channel


class Future(Channel):
    def get_name(self) -> str:
        return 'Future TV'

    def get_logo(self) -> str:
        return 'http://www.futuretvnetwork.com/demo/wp-content/uploads/2014/05/goodnews-rtl.png'

    def get_stream_url(self) -> str:
        return 'http://futuretv.cdn.mangomolo.com/futuretv/futuretv/playlist.m3u8'

    def get_epg_data(self):
        return None
