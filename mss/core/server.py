# coding: utf-8
#!/usr/bin/env python

from tornado.httpserver import HTTPServer
from tornado.web import Application, StaticFileHandler, RequestHandler, HTTPError
from tornado.ioloop import IOLoop
from mss.handler.base import BaseHandler
from mss.core import settings
from mss.core.daemon import Daemon

import cProfile as profile

import re, logging, sys

get_controller = None
get_mapper = None

COOKIE_SECRET = "29NbhyfgaA092ZkjMbNvCx06789jdA8iIlLqz7d1D9c8"


class MSSServer(Daemon):

    def __init__(self, pidfile, port, root, controller, mapper, media):
        self.port = port
        self.root = root
        self.media = media
        global get_controller, get_mapper
        get_controller = controller
        get_mapper = mapper

        return Daemon.__init__(self, pidfile)

    def run(self):

        application = Application([
            (r"/media/(.*)", StaticFileHandler, {"path": self.media}),
            (r"/.*", MSSHandler)
        ], cookie_secret=COOKIE_SECRET)

        http_server = HTTPServer(application, xheaders=True)
        http_server.listen(self.port)

        logging.info("MSS Server START! listening port %s " % self.port)

        IOLoop.instance().start()


class MSSHandler(RequestHandler):

    def process_request(self, *args, **kargs):
        global get_controller, get_mapper
        mapper = get_mapper()

        # remove get args
        uri = re.sub("\?.*", "", self.request.uri)

        match = mapper.match(uri)
        if match:
            try:
                controller = get_controller(match['controller'], settings.DEBUG)

                karguments = self.prepared_arguments(match)
                karguments['request_handler'] = self

                response = getattr(controller, match['action'])(**karguments)

                if not response: return
                self.write(response)
            
            except Exception, e:
                if hasattr(e,'status_code') and e.status_code == 404:
                    logging.info("404 - Pagina nao encontrada %s" % self.request.uri) 
                    self.write(BaseHandler().render_to_template("/404.html"))
                else:
                    logging.exception("500 - Erro ao processar a requisicao %s" % e)
                    if settings.DEBUG:
                        raise HTTPError(500)
                    else:
                        self.write(BaseHandler().render_to_template("/500.html"))
        else:
            logging.info("404 - Pagina nao encontrada %s" % self.request.uri)
            
            if settings.DEBUG:
                raise HTTPError(404)
            else:
                self.write(BaseHandler().render_to_template("/404.html"))
    
    def get(self, *args, **kw):
        logging.debug("GET %s processing..." % self.request.uri)
        if settings.PROFILING:
            self.profiling(*args, **kw)
        else:
            self.process_request(*args, **kw)
    
    def post(self, *args, **kw):
        logging.debug("POST %s processing..." % self.request.uri)
        if settings.PROFILING:
            self.profiling(*args, **kw)
        else:
            self.process_request(*args, **kw)

    def prepared_arguments(self, match):
        arguments = {}
        for arg,value in self.request.arguments.iteritems():
            arguments[arg] = value[0]
            
        for key,value in match.iteritems():
            if key not in ('controller','action'):
                arguments[key] = value
                        
        return arguments

    def profiling(self, *args, **kw):
        self.profiler = profile.Profile()

        self.profiler.runcall(self.process_request, *args, **kw)

        self.profiler.dump_stats(settings.PROFILE_FILE)