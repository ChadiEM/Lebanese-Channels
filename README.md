# Lebanese channels for Kodi & IPTV-Simple, with limited XMLTV EPG support

## Requirements
- [Kodi](https://kodi.tv/)
- Kodi PVR add-on: [IPTV-Simple](http://kodi.wiki/view/Add-on:IPTV_Simple_Client)
- Python 3 & Modules:
  - flask
  - flask_cache
  - gunicorn
  - BeatifulSoup4
  - lxml

## Run
./start.sh

## Configure
Configure Kodi IPTV-Simple client to use:
- `http://localhost:12589/channels` as channels URL
- `http://localhost:12589/epg` as EPG URL

## Output
![Example Output](http://i.imgur.com/sDKK2H0.jpg)