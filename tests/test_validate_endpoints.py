import unittest
import urllib
import urllib.request
from urllib.error import HTTPError

from lebanese_channels.channel import StreamError, StreamNotFoundError
from lebanese_channels.channel_ids import CHANNEL_LIST


class ValidationTest(unittest.TestCase):
    """The below tests are purely informative.

    No assertions are done as these tests are not necessarily reproducible
    (some streams might be down at the time tests are run)

    """

    def test_logos(self):
        for channel in CHANNEL_LIST:
            print('Checking ' + channel.get_name() + '...')
            self.check_status(channel.get_logo())

    def test_streams(self):
        for channel in CHANNEL_LIST:
            print('Checking ' + channel.get_name() + '...')
            try:
                self.check_status(channel.get_stream_url())
            except (StreamError, StreamNotFoundError):
                print('Invalid: <unable to fetch stream url>')

    @staticmethod
    def check_status(url):
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
