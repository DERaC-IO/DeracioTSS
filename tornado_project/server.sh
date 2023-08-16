#!/usr/bin/bash

# Define the app name
APP_NAME="DeracioTSS -- A Tornado/Python Startup Script"

# Full path to the app directory
HOME_DIR=`pwd`

# Full path to the server program
# Tornado launches webserver of itself => path to python
SERVER="$HOME_DIR/.pypy/bin/python"

# App file name that includes 'application' to 'listen'
### For example:
### application = tornado.web.Application(...)
### application.listen(...)
APP="app.py"

# Startup script
echo "Starting $APP_NAME"
$SERVER $HOME_DIR/$APP
