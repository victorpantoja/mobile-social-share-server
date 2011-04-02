# coding: utf-8
#!/usr/bin/env python

import inspect, re, logging, hashlib
from sqlalchemy.orm.query import Query
from sqlalchemy.orm import attributes, MapperExtension, EXT_CONTINUE, EXT_STOP
from sqlalchemy.orm.session import Session
from sqlalchemy.exceptions import InvalidRequestError
from datetime import datetime
from mss.core import settings
from mss.core.cache.util import get_cache, cache_key

class CachedQuery(Query):
    
    @staticmethod
    def generate_key(obj, id):
        
        if type(id) == list:
            id = id[0]
        cache_key = "%s.%s(%s)" % (obj.__module__, obj.__name__, id)
        
        logging.debug("CachedQuery -> generate key %s" % cache_key)
        
        return hashlib.md5(cache_key).hexdigest(), cache_key
    
    def get(self, ident, **kw):
    
        mapper = self._mapper_zero()
        session = self.session
        cache = get_cache()
        
#        logging.debug("%s.................................................." % datetime.now().strftime("%H:%M:%S:%f"))
        
        key = mapper.identity_key_from_primary_key(ident)
        
        cacheobj = session.identity_map.get(key)
        
        if cacheobj and hasattr(cacheobj, "__no_session__") and cacheobj.__no_session__:
            session.expunge(cacheobj)
            cacheobj = None

        cache_key, keystr = CachedQuery.generate_key(key[0], ident)

        if not cacheobj:

            if not (hasattr(key[0], "__no_cache__") and key[0].__no_cache__):
                cacheobj = cache.get(cache_key)

            if cacheobj is not None:
                logging.debug("CachedQuery [CACHE] -> recuperando do cache e setando na sessao")
                cacheobj.__dict__["_sa_instance_state"] = attributes.instance_state(cacheobj)
                session.add(cacheobj)
                    
            else:
                logging.debug("CachedQuery [BANCO] -> nao existe no cache, pega do banco %s" % keystr)
                cacheobj = super(CachedQuery, self).get(ident)
                if cacheobj is None: 
                    return None 
                logging.debug("CachedQuery [CACHE] -> setando no cache %s" % cacheobj)
                cache.set(cache_key, cacheobj)
        else:
            logging.debug("CachedQuery [SESSION] -> recuperando da sessao ")

#        logging.debug("%s.................................................." % datetime.now().strftime("%H:%M:%S:%f"))
        return cacheobj
        
class CachedExtension(MapperExtension):

    def get_key_from_mapper(self, mapper, instance):
        mapperkey = mapper.identity_key_from_instance(instance)
        key = "%s.%s(%s)" % (mapperkey[0].__module__,mapperkey[0].__name__,int(mapperkey[1][0]))
        md5key = hashlib.md5(key).hexdigest()
        return md5key, key
    
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
    
    def load_model(self, module, classe):
        mod = __import__("mss.models.%s" % module, fromlist=[classe])
        return getattr(mod, classe)()
    
    def get_key_from_expires(self, instance, expire):
        match = re.search("(?P<module>\w+)\.(?P<method>[^\(]+)\((?P<params>[^\)]*)\)",expire)
        if match:
            result = match.groupdict()
            
            expire_instance = self.load_model(result['module'].lower(), result['module'])
            
            kwarguments = self.prepare_parameters(instance, result['params'])
            
            return cache_key(expire_instance, result['method'], **kwarguments)
            
        return None
        
    def get_expires(self,instance, action):
        if hasattr(instance, "__expires__"):
            expires = instance.__expires__.get(action)
            if expires:
                return expires
        return []
            
    def after_insert(self, mapper, connection, instance):
        cache = get_cache()
        expires = self.get_expires(instance, "create")
        for expire in expires:
            md5key, key = self.get_key_from_expires(instance, expire)
            logging.debug("Invalidando chave[%s] no cache on insert [%s]" % (key,instance))
            cache.delete(md5key)
        
        return EXT_CONTINUE

    def after_update(self, mapper, connection, instance):
        if not Session.object_session(instance).is_modified(instance, include_collections=False, passive=True): return EXT_STOP
        
        cache = get_cache()
        expires = self.get_expires(instance, "update")
        for expire in expires:
            md5key, key = self.get_key_from_expires(instance, expire)
            logging.debug("Invalidando chave[%s] no cache on update [%s]" % (key,instance))
            cache.delete(md5key)

        # espira a instancia
        md5key, key = self.get_key_from_mapper(mapper,instance)
        logging.debug("Invalidando chave[%s] no cache on update [%s]" % (key,instance))
        cache.delete(md5key)
        
        return EXT_CONTINUE
        
    def after_delete(self, mapper, connection, instance):
        cache = get_cache()
        expires = self.get_expires(instance, "delete")
        for expire in expires:
            md5key, key = self.get_key_from_expires(instance, expire)
            logging.debug("Invalidando chave[%s] no cache on delete [%s]" % (key,instance))
            cache.delete(md5key)

        # espira a instancia
        md5key, key = self.get_key_from_mapper(mapper,instance)
        logging.debug("Invalidando chave[%s] no cache on delete [%s]" % (key,instance))
        cache.delete(md5key)
        
        return EXT_CONTINUE