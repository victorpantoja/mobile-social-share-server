# coding: utf-8
#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.interfaces import ConnectionProxy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.interfaces import SessionExtension
from tornado.options import options
import logging
import time

__session__ = None
__engine_readable__ = None
__engine_writable__ = None
_MODELS = {}

class TimerProxy(ConnectionProxy):
    def cursor_execute(self, execute, cursor, statement, parameters, context, executemany):
            
        now = time.time()
        try:
            return execute(cursor, statement, parameters, context)
        finally:
            total = time.time() - now
            logging.debug("Query: %s" % statement)
            logging.debug("Total Time: %f" % total)

class UndefinedModel(Exception):
    pass

class CartolaSessionExtension(SessionExtension):
    def before_flush(self, session, flush_context, instances):
        session.bind = get_engine(writable=True, max_overflow=10)
        
def get_model(name):
    try:
        return _MODELS[name]
    except KeyError:
        raise UndefinedModel, "The model %s does not exist, perharps it hasn't been imported" % name

def get_engine(writable=False, **kw):
    if writable:
        global __engine_writable__
        if not __engine_writable__:
            __engine_writable__ = create_engine(options.DATABASE_ENGINE['write'], pool_size=options.DATABASE_POOL_SIZE, pool_recycle=300, proxy=TimerProxy(), **kw)
        return __engine_writable__
    else:
        global __engine_readable__
        if not __engine_readable__:
            __engine_readable__ = create_engine(options.DATABASE_ENGINE['read'], pool_size=options.DATABASE_POOL_SIZE, pool_recycle=300, proxy=TimerProxy(), **kw)
        return __engine_readable__
    
def get_session(writable=False):
    global __session__
    if not __session__:
        __session__ = scoped_session(sessionmaker(autocommit=True, autoflush=False, expire_on_commit=False))
    engine = get_engine(writable=writable, max_overflow=10)
    __session__.bind = engine
    return __session__()