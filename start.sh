#!/bin/bash
gunicorn -c gunicorn.ini flaskapp:app
