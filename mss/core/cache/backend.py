# coding: utf-8
#!/usr/bin/env python

from mss.utils.encoding import smart_unicode, smart_str
import logging
import memcache

class MemcachedClass():

    def __init__(self, server, timeout):
        self.server = server
        self.default_timeout = int(timeout)
        self._cache = memcache.Client(self.server)
        logging.debug("Memcached start client %s" % server)

    def add(self, key, value, timeout=0):
        if isinstance(value, unicode):
            value = value.encode('utf-8')

        try:
            return self._cache.add(smart_str(key), value, timeout or self.default_timeout)
        except:
            logging.exception("memcache server desligado!")

    def get(self, key, default=None):
        try:
            val = self._cache.get(smart_str(key))
            if val is None:
                return default
            else:
                if isinstance(val, basestring):
                    return smart_unicode(val)
                else:
                    return val
        except:
            logging.exception("memcache server desligado!")
            return None

    def set(self, key, value, timeout=0):
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        self._cache.set(smart_str(key), value, timeout or self.default_timeout)

    def delete(self, key):
        self._cache.delete(smart_str(key))

    def get_many(self, keys):
        return self._cache.get_multi(map(smart_str, keys))

    def close(self, **kwargs):
        self._cache.disconnect_all()
       
    def stats(self):
        try:
            return self._cache.get_stats()
        except Exception:
            logging.exception("memcache server desligado!")
     
    def flush_all(self):
        try:
            self._cache.flush_all()
        except Exception:
            logging.exception("memcache server desligado!")
