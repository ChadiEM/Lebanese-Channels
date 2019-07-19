# Lebanese Channels Playlist

This Python module consists of a web server that provides a `/channels` endpoint for a playlist of some of the most common Lebanese channels.

## Run
`./start.sh` to start the server.
Or, if using docker, `docker run -d -p 12589:12589 chadiem/lebanese-channels`

## Configure
- Kodi:
  - Install Kodi PVR add-on: [IPTV-Simple](http://kodi.wiki/view/Add-on:IPTV_Simple_Client)
  - Configure Kodi IPTV-Simple client to use:
    - `http://<hostname>:12589/channels` as channels URL
- VLC:
  - Media > Open Network Stream > `http://<hostname>:12589/channels`
