#!/bin/sh

gunicorn --bind :12589 --timeout=60 lebanese_channels.flask_app:app
