# coding: utf-8
#!/usr/bin/env python

import inspect, re, logging, hashlib
from datetime import datetime
from mss.core import settings
from mss.core.cache.backend import MemcachedClass, RedisClass

__cache__ = None
def get_cache():
    global __cache__
    if not __cache__:
        if settings.CACHE_BACKEND == "memcached":
            servers = settings.CACHE_BACKEND_OPTS[settings.CACHE_BACKEND]
            __cache__ = MemcachedClass(servers, settings.CACHE_TIMEOUT)
        elif settings.CACHE_BACKEND == "redis":
            master = settings.CACHE_BACKEND_OPTS[settings.CACHE_BACKEND]["master"]
            slave = settings.CACHE_BACKEND_OPTS[settings.CACHE_BACKEND]["slave"]
            __cache__ = RedisClass(master, slave, settings.CACHE_TIMEOUT)

    return __cache__

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
        if arg != 'self':
            params[arg] = ""

    for name, value in kwarguments.iteritems():
        if value:
            params[name] = value.replace(' ','') if isinstance(value,str) else value
    
    keys = params.keys()
    keys.sort()
    
    cachekey = cachekey.replace("{params}", ",".join(["%s=%s" % (key, params[key]) for key in keys]))
    md5key = hashlib.md5(cachekey).hexdigest()
    
    return md5key, cachekey

def cached_method(fn, *arguments, **kwarguments):

    if len(arguments) == 0 :
#       return fn(*arguments, **kwarguments)
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
            
        logging.debug("SET IN CACHE %s" % result)
    else:
        logging.debug("GET FROM CACHE")
    return result

def cached(fn):    
    def cached_static_fn(*args, **kw):
        return cached_method(fn, *args, **kw)
    # hack for access decorated function
    cached_static_fn.fn = fn
    
    return cached_static_fn

def cached_timeout(timeout):
    def cached(fn):
        def cached_static_fn(*arguments, **kwarguments):
            fn.timeout = timeout
            return cached_method(fn, *arguments, **kwarguments)

        # hack for access decorated function
        cached_static_fn.fn = fn

        return cached_static_fn
    
    return cached
    
'''
    expire decorated method from cache
'''
def expire_key(method, **kw):
    if method.__name__ != 'cached_static_fn':
        raise ValueError("Somente metodos decorados com cached, podes ser expirados")

    md5key, key = cache_key(method.im_class(), method.fn.__name__ , **kw)
    
    cache = get_cache()
    logging.debug("[CACHE][expire] - %s {%s}" % (md5key, key))

    cache.delete(md5key)

'''
    set value as decorated method in cache
'''
def set_key(method, value, **kw):
    if method.__name__ != 'cached_static_fn':
        raise ValueError("Somente metodos decorados com cached, podes ser expirados")

    md5key, key = cache_key(method.im_class(), method.fn.__name__ , **kw)
    
    cache = get_cache()
    logging.debug("[CACHE][set] - %s {%s}" % (md5key, key))

    cache.set(md5key, value)

