# coding: utf-8
#!/usr/bin/env python

from mss.core.cache.util import get_cache, cache_key

import re, logging, hashlib

class CachedExtension():
    
    def after_insert(self, instance):
        cache = get_cache()
        expires = self.get_expires(instance, "create")
        for expire in expires:
            md5key, key = self.get_key_from_expires(instance, expire)
            logging.debug("Invalidando chave[%s] no cache no insert [%s]" % (key,instance))
            cache.delete(md5key)
            
    def after_delete(self, instance):
        cache = get_cache()
        expires = self.get_expires(instance, "delete")
        for expire in expires:
            md5key, key = self.get_key_from_expires(instance, expire)
            logging.debug("Invalidando chave[%s] no cache no delete [%s]" % (key,instance))
            cache.delete(md5key)

        return
            
    def get_expires(self,instance, action):
        if hasattr(instance, "__expires__"):
            expires = instance.__expires__.get(action)
            if expires:
                return expires
        return []
            
    def get_key_from_expires(self, instance, expire):        
        match = re.search("(?P<module>\w+)\.(?P<method>[^\(]+)\((?P<params>[^\)]*)\)",expire)
        
        if match:
            result = match.groupdict()

            expire_instance = self.load_model(result['module'].lower(), result['module'])

            kwarguments = self.prepare_parameters(instance, result['params'])

            # method nao decorado
            if not hasattr(getattr(expire_instance, result['method']), 'fn'):
                cachekey = "%(module)s.%(method)s({params})" % result
                cachekey = cachekey.replace("{params}", ",".join(["%s=%s" % (key, value) for key, value in kwarguments.iteritems()]))

                return hashlib.md5(cachekey).hexdigest(), cachekey
            
            return cache_key(expire_instance, result['method'], **kwarguments)

        return None

    def load_model(self, module, classe):
        mod = __import__("newsfeed.models.%s" % module, fromlist=[classe])
        return getattr(mod, classe)()
        
    def prepare_parameters(self, instance, params):
        result = {}

        if params != '':
            for param in params.split(","):
                arg = param.split("=")
                value = instance
                for attr in arg[1].split("."):
                    value = getattr(value,attr)
                result[arg[0].strip()] = value
        return result
        
        
class CachedQuery():

    @staticmethod
    def generate_key(obj, id):

        if type(id) == list:
            id = id[0]
        cache_key = "%s.%s(%s)" % (obj.__module__, obj.__class__.__name__, id)
        
        md5key = hashlib.md5(cache_key).hexdigest()

        logging.debug("CachedQuery -> generate key %s no formato md5 %s" % (cache_key, md5key))

        return md5key, cache_key

    def get(self, id):

        cache = get_cache()

        md5key, cache_key = CachedQuery.generate_key(self, id)

        cacheobj = cache.get(md5key)

        if cacheobj is not None:
            logging.debug("CachedQuery [CACHE] -> recuperando do cache")
        else:
            logging.debug("CachedQuery [BANCO] -> nao existe no cache, pega do banco %s" % cache_key)
            
            self.get_collection().find_one({'id':id},callback=self.on_findone)

            
    def on_findone(self,response,error):
        
        #if error...
        cacheobj = response
        if cacheobj is None: 
            return None
        
        cache = get_cache()
        md5key, cache_key = CachedQuery.generate_key(self, str(cacheobj['id']))
        
        logging.debug("CachedQuery [CACHE] -> setando no cache %s" % cacheobj)

        cache.set(md5key, cacheobj)
        return cacheobj