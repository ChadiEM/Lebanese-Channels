#!/bin/bash

env python3 lebanese_channels/entry_point.py -b :12589 --timeout=60 lebanese_channels.flask_app:wsgi_app
