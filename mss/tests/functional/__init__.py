# coding: utf-8
#!/usr/bin/env python

from datetime import datetime

import tornado.options
import os, sys, logging, hashlib

project_root = os.path.abspath(os.path.dirname(__file__))

tornado.options.define("port", type=int, default=9080, help="port to listen")
tornado.options.define("conf", default="settings.py", help="config file")
tornado.options.define("pidfile", type=str, default="/opt/logs/mss/mss.pid", help="pidfile")
tornado.options.define("as_daemon", type=bool, default=False, help="run server as daemon")
tornado.options.define("template_dir", type=str, default="%s/templates" % project_root)
tornado.options.define("media_dir", type=str, default="%s/media" % project_root)
tornado.options.define("EMAIL", type=dict)
tornado.options.define("DATABASE_ENGINE", type=dict, default={"read":"mysql://root@localhost/mss?charset=utf8&use_unicode=0", "write":"mysql://root@localhost/mss?charset=utf8&use_unicode=0"})
tornado.options.define("DATABASE_POOL_SIZE", type=int, default=25)

logging.getLogger().setLevel(getattr(logging, "error"))
