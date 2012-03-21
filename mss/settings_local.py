# coding: utf-8
#!/usr/bin/env python

import logging
import os

DEBUG = True
PROFILING = False
PROFILE_FILE = "/opt/logs/mss/profiler.out.log"

DATABASE_ENGINE = {
    "read":"mysql://root@localhost/mss?charset=utf8&use_unicode=0",
    "write":"mysql://root@localhost/mss?charset=utf8&use_unicode=0"
}

DATABASE_POOL_SIZE = 25

logging.basicConfig(
    level = getattr(logging, "DEBUG"),
    format = '%(asctime)s %(levelname)s %(message)s',
#    filename = "/opt/logs/cartola/python-fe/cartola.log",
#    filemode = 'a'
)
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

MSS_BOXES = ["localhost"]

CACHE_BACKEND_OPTS = {
    "memcached": ["%s:11211" % box for box in MSS_BOXES],
    "redis":{
        "master":"localhost:6379",
        "slave":"localhost:6379"
    }
}

CACHE_BACKEND = "memcached"
CACHE_TIMEOUT = 63300

BEANSTALK_BOXES = ["localhost"]
BEANSTALK = "localhost:11300"
BEANSTALK_HOSTS = ["%s:11300" % box for box in BEANSTALK_BOXES]

TEMPLATE_DIRS = [
    "%s/templates" % os.path.abspath(os.path.dirname(__file__)),
]

EMAIL = {
    "server":"smtp.gmail.com",
    "port":25,
}