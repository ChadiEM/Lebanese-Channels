# Archival Notice

As the channels are no longer freely accessible, this project is no longer relevant.

# Lebanese Channels Playlist

This Python module consists of a web server that provides a `/channels` endpoint for a playlist of some of the most
common Lebanese channels.

## Run

### Docker

The easiest way to experiment with this module is to run it using docker.

`docker run -d -p 12589:12589 chadiem/lebanese-channels`

### Local
```
pip install -r requirements.txt
./start.sh
```

## Configure
- Kodi:
  - Install Kodi PVR add-on: [IPTV-Simple](http://kodi.wiki/view/Add-on:IPTV_Simple_Client)
  - Configure Kodi IPTV-Simple client to use:
    - `http://<hostname>:12589/channels` as channels URL
- VLC:
  - Media > Open Network Stream > `http://<hostname>:12589/channels`