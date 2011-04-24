# coding: utf-8
#!/usr/bin/env python

from mss.core.cache.extension import CachedQuery, CachedExtension
from mss.core.cache.util import get_cache, cache_key, cached
import logging

__all__ = (
    'CachedQuery',
    'CachedExtension',
    'get_cache',
    'cache_key',
    'cached',
    'cached_timeout'
)


'''
    set value as decorated method in cache
'''
def set_instance_cache(instance):
    md5key, key = CachedQuery.generate_key(instance.__class__, instance.id)
    cache = get_cache()
    logging.debug("[CACHE][set] - %s {%s}" % (md5key, key))

    cache.set(md5key, instance)


def expire_instance_cache(classe, id):
    md5key, key = CachedQuery.generate_key(classe, id)
    cache = get_cache()
    logging.debug("[CACHE][expire] - %s {%s}" % (md5key, key))

    cache.delete(md5key)
