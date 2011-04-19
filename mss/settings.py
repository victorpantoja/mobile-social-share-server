# coding: utf-8
#!/usr/bin/env python

log_file_prefix = "/opt/logs/mss/mss.log"
logging='debug'

EMAIL = {
    "server":"smtpar.globoi.com",
    "port":25,
}

DATABASE_ENGINE = {
    "read":"mysql://root@localhost/mss?charset=utf8&use_unicode=0",
    "write":"mysql://root@localhost/mss?charset=utf8&use_unicode=0"
}

MSS_BOXES = [ "localhost" ]

DATABASE_POOL_SIZE = 25

CACHE_BACKEND_OPTS = {
    "memcached": ["%s:11211" % box for box in MSS_BOXES],
    "redis":{
        "master":"localhost:6379",
        "slave":"localhost:6379"
    }
}

CACHE_BACKEND = "memcached"
CACHE_TIMEOUT = 63300