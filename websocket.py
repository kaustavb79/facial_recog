#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging as log
import os
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options
from api_face_recog.src.detect_face import get_face_detect_data


def setup_custom_logger(name):
    formatter = log.Formatter(fmt='%(asctime)s - %(process)d - %(levelname)s - %(message)s')
    handler = log.StreamHandler()
    handler.setFormatter(formatter)
    logger = log.getLogger(name)
    logger.setLevel(log.INFO)
    logger.addHandler(handler)
    return logger


logger = setup_custom_logger("tornado_websocket")


define("port", default=8002, help="run on the given port", type=int)

class MainHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        logger.info("A client connected.")

    def on_close(self):
        logger.info("A client disconnected")

    def on_message(self, message):
        image_data = get_face_detect_data(message)
        if not image_data:
            image_data = message
        self.write_message(image_data)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/websocket", MainHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "face_recog.settings")
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()