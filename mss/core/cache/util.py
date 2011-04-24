# coding: utf-8
#!/usr/bin/env python

from mss.core.cache.backend import MemcachedClass
from tornado.options import options

import inspect, logging, hashlib

__cache__ = None
def get_cache():
    global __cache__
    if not __cache__:
        servers = options.CACHE_BACKEND_OPTS
        __cache__ = MemcachedClass(servers, options.CACHE_TIMEOUT)
    return __cache__
        
def cached_method(fn, *arguments, **kwarguments):

    if len(arguments) == 0 :
        raise ValueError("Somente metodods de instancia podem ser cacheados")

    md5key, key = cache_key(arguments[0], fn.__name__, **kwarguments)

    logging.debug("verificando chave %s no cache no formato md5 %s  " % (key, md5key))
    cache = get_cache()
    result = cache.get(md5key)

    if result is None:
        result = fn(*arguments, **kwarguments)
        if hasattr(fn, 'timeout'):
            cache.set(md5key, result, fn.timeout)
        else:
            cache.set(md5key, result)

        logging.debug("SET IN CACHE %s" % (result))
    else:
        logging.debug("GET FROM CACHE")
    return result

def cached(fn):    
    def cached_static_fn(*args, **kw):
        return cached_method(fn, *args, **kw)
    # hack for access decorated function
    cached_static_fn.fn = fn

    return cached_static_fn
    
    
def cache_key(instance, method, **kwarguments):
    cachekey = "{module}.{classe}({instanceid}).{method}({params})"

    cachekey = cachekey.replace("{module}",instance.__module__)
    cachekey = cachekey.replace("{classe}",instance.__class__.__name__)
    cachekey = cachekey.replace("{method}",method)

    if hasattr(instance, "id") and instance.id:
        cachekey = cachekey.replace("{instanceid}","%s" % instance.id)
    else:
        cachekey = cachekey.replace("{instanceid}","")

    params = {}

    argspected = inspect.getargspec(getattr(instance, method).fn).args
    for arg in argspected:
        if arg != 'self' and arg != 'callback':
            params[arg] = ""

    for name, value in kwarguments.iteritems():
        if name != 'callback':
            if value:
                params[name] = value.replace(' ','') if isinstance(value,str) else value

    keys = params.keys()
    keys.sort()
    cachekey = cachekey.replace("{params}", ",".join(["%s=%s" % (key, params[key]) for key in keys]))
    md5key = hashlib.md5(cachekey).hexdigest()

    return md5key, cachekey