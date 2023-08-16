#!/home/ecs-user/japorn/.pypy/bin/python
# -*- coding: utf-8 -*-
import tornado.ioloop, tornado.web
import os, re, json, threading

# Define fundamental parameters for the service
# These params can be alternatively in, i.e., settings.py
__port__ = 8000
__templates__ = "templates"
__static__ = "static"

# Classes are separately stored in external files
# Follow the structure rule of each project
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        params = {
            'title': 'Deracio Tornado/Python Setupper'
        }
        self.render("index.html", params = params)

# Definition for the web service
# Routing, debug (autoload) setting, template/static folders, etc...
application = tornado.web.Application(
    [
        ("/", MainHandler),
    ],
    debug=True,
    template_path=os.path.join(os.getcwd(), __templates__),
    static_path=os.path.join(os.getcwd(), __static__),
)

# Startup script for the server (read by server.sh)
if __name__ == "__main__":
    application.listen(__port__)
    tornado.ioloop.IOLoop.instance().start()
