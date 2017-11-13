import unittest
import urllib
from urllib.error import HTTPError

from lebanese_channels.channel_ids import CHANNEL_LIST
from lebanese_channels.stream.stream_fetcher import StreamError


class ValidationTest(unittest.TestCase):
    """The below tests are purely informative.

    No assertions are done as these tests are not necessarily reproducible
    (some streams might be down at the time tests are run)

    """

    def test_logos(self):
        for channel in CHANNEL_LIST:
            print('Checking ' + channel.name + '...')
            self.check_status(channel.logo)

    def test_direct_streams(self):
        for channel in CHANNEL_LIST:
            if channel.url is not None:
                print('Checking ' + channel.name + '...')
                self.check_status(channel.url)

    def test_streams_fetchers(self):
        for channel in CHANNEL_LIST:
            if channel.stream_fetcher is not None:
                print('Checking ' + channel.name + '...')
                try:
                    url = channel.stream_fetcher.fetch_stream_url()
                    self.check_status(url)
                except StreamError:
                    print('Invalid: <unable to fetch stream url>')

    def check_status(self, url):
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0')
        try:
            response = urllib.request.urlopen(req)
            if response.code == 200:
                print('Valid: ' + url)
            else:
                print('Invalid: ' + url)
        except HTTPError:
            print('Invalid: ' + url)


if __name__ == "__main__":
    unittest.main()
