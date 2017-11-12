class EPGURL:
    def __init__(self, url: str, data=None):
        self._url = url
        self._data = data

    @property
    def url(self) -> str:
        return self._url

    @property
    def data(self) -> str:
        return self._data
