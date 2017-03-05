# Lebanese Channels Playlist & EPG

This Python module is a web server that provides two endpoints:
- A `/channels` endpoint for a playlist of some of the most common Lebanese channels, in m3u8 format.
- An `/epg` endpoint for EPG fetched from their corresponding websites, in XMLTV format.

## Requirements
- Python 3 & Modules:
  - flask
  - flask_caching
  - gunicorn
  - BeautifulSoup4
  - lxml
  - pytz

## Run
`./start.sh` to start the server.

## Configure
- Kodi:
  - Install Kodi PVR add-on: [IPTV-Simple](http://kodi.wiki/view/Add-on:IPTV_Simple_Client)
  - Configure Kodi IPTV-Simple client to use:
    - `http://<hostname>:12589/channels` as channels URL
    - `http://<hostname>:12589/epg` as EPG URL
- VLC:
  - Media > Open Network Stream > `http://<hostname>:12589/channels`