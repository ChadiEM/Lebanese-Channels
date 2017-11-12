import urllib
import urllib.parse
import urllib.request


def get_response(url: str, params=None):
    data = None if params is None else urllib.parse.urlencode(params).encode('utf-8')
    req = urllib.request.Request(url, data=data)

    req.add_header('User-Agent',
                   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0')

    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    response.close()
    return html
