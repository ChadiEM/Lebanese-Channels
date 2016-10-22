import urllib
import urllib.parse
import urllib.request

from epg_data import PostURL


def get_html_response_for(url: str) -> str:
    req = urllib.request.Request(url)
    req.add_header('Accept', 'text/html')
    req.add_header('User-Agent',
                   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0')
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    response.close()
    return html


def get_post_html_response_for(post_data: PostURL) -> str:
    req = urllib.request.Request(
        post_data.url,
        data=urllib.parse.urlencode(post_data.params).encode('utf-8'),
        method="POST")

    req.add_header('User-Agent',
                   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0')

    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    response.close()
    return html
