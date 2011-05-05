# coding: utf-8
#!/usr/bin/env python

from datetime import datetime

from tornado import options
import os, sys, logging, hashlib

project_root = os.path.abspath(os.path.dirname(__file__))

options.define("port", type=int, default=9080, help="port to listen")
options.define("conf", default="settings.py", help="config file")
options.define("pidfile", type=str, default="/opt/logs/mss/mss.pid", help="pidfile")
options.define("as_daemon", type=bool, default=False, help="run server as daemon")
options.define("template_dir", type=str, default="%s/templates" % project_root)
options.define("media_dir", type=str, default="%s/media" % project_root)
options.define("EMAIL", type=dict, default={"server":"smtp.gmail.com","port":25,})
options.define("DATABASE_ENGINE", type=dict, default={"read":"mysql://root@localhost/mss?charset=utf8&use_unicode=0", "write":"mysql://root@localhost/mss?charset=utf8&use_unicode=0"})
options.define("DATABASE_POOL_SIZE", type=int, default=25)
options.define("CACHE_BACKEND_OPTS", multiple=True, default=["localhost:11211"])
options.define("CACHE_TIMEOUT", type=int, default=63300)

logging.getLogger().setLevel(getattr(logging, "error"))
