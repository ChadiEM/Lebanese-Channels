#!/bin/bash
gunicorn -b :12589 flaskapp:app
