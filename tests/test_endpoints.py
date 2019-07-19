import unittest

from lebanese_channels.flask_app import app


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_channels(self):
        response = self.app.get('/channels')
        self.assertTrue('#EXTM3U' in response.data.decode('utf-8'))


if __name__ == "__main__":
    unittest.main()
