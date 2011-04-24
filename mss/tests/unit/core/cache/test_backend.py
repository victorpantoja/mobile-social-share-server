# coding: utf-8
#!/usr/bin/env python

from mox import Mox
from mss.core.cache import backend


def test_can_be_init_memcache():
    mox = Mox()
    
    mox.StubOutWithMock(backend,'memcache', use_mock_anything=True)
    
    servers = ["localhost:11211","localhost:11212"]
    backend.memcache.Client(servers).AndReturn(True)
    
    mox.ReplayAll()
    try:
        cache = backend.MemcachedClass(server=servers,timeout=30)
        assert cache._cache
        assert cache.default_timeout == 30

        mox.VerifyAll()
    finally:
        mox.UnsetStubs()
        
def test_can_be_add():
    mox = Mox()
    
    key = "should-be-key"
    value = u"should-be-value"
    timeout = "should-be-timeout"

    mox.StubOutWithMock(backend,'memcache', use_mock_anything=True)
    
    cache_mock = mox.CreateMockAnything()
    cache_mock.add(key, value, timeout).AndReturn(value)
    
    backend.memcache.Client(["localhost:11211"]).AndReturn(cache_mock)
    
    mox.ReplayAll()
    try:
        memcache = backend.MemcachedClass(server=["localhost:11211"],timeout=30)
        assert memcache.add(key, value, timeout) == "should-be-value"
    
        mox.VerifyAll() 
    finally:
        mox.UnsetStubs()

def test_can_be_get():
    mox = Mox()
    
    key = "should-be-key"
    value = u"should-be-value"

    mox.StubOutWithMock(backend,'memcache', use_mock_anything=True)
    
    cache_mock = mox.CreateMockAnything()
    cache_mock.get(key).AndReturn(value)
    
    backend.memcache.Client(["localhost:11211"]).AndReturn(cache_mock)
    
    mox.ReplayAll()
    try:
        memcache = backend.MemcachedClass(server=["localhost:11211"],timeout=30)
        assert memcache.get(key) == value
        
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()        

def test_can_be_get_default():
    mox = Mox()
    
    key = "should-be-key"

    mox.StubOutWithMock(backend,'memcache', use_mock_anything=True)
    
    cache_mock = mox.CreateMockAnything()
    cache_mock.get(key).AndReturn(None)
    
    backend.memcache.Client(["localhost:11211"]).AndReturn(cache_mock)
    
    mox.ReplayAll()
    try:
        memcache = backend.MemcachedClass(server=["localhost:11211"],timeout=30)
        assert memcache.get(key, default="should-be-value-default") == "should-be-value-default"
        
    finally:
        mox.UnsetStubs()

def test_can_be_get_object():
    mox = Mox()
    
    class MockObject(object):
        pass
    
    mockobject = MockObject()
    key = "should-be-key"
    value = mockobject

    mox.StubOutWithMock(backend,'memcache', use_mock_anything=True)
    
    cache_mock = mox.CreateMockAnything()
    cache_mock.get(key).AndReturn(value)
    
    backend.memcache.Client(["localhost:11211"]).AndReturn(cache_mock)
    
    mox.ReplayAll()
    try:
        memcache = backend.MemcachedClass(server=["localhost:11211"],timeout=30)
        assert memcache.get(key) == value
        
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_can_be_set():
    mox = Mox()
    
    key = "should-be-key"
    value = u"should-be-value"
    timeout = "should-be-timeout"

    mox.StubOutWithMock(backend,'memcache', use_mock_anything=True)
    
    cache_mock = mox.CreateMockAnything()
    cache_mock.set(key, value, timeout).AndReturn(value)
    
    backend.memcache.Client(["localhost:11211"]).AndReturn(cache_mock)
    
    mox.ReplayAll()
    try:
        memcache = backend.MemcachedClass(server=["localhost:11211"],timeout=30)
        memcache.set(key, value, timeout)

        mox.VerifyAll()
    finally:
        mox.UnsetStubs()
        
def test_can_be_delete():
    mox = Mox()
    
    key = "should-be-key"

    mox.StubOutWithMock(backend,'memcache', use_mock_anything=True)
    
    cache_mock = mox.CreateMockAnything()
    cache_mock.delete(key)
    
    backend.memcache.Client(["localhost:11211"]).AndReturn(cache_mock)
    
    mox.ReplayAll()
    try:
        memcache = backend.MemcachedClass(server=["localhost:11211"],timeout=30)
        memcache.delete(key)

        mox.VerifyAll()
    finally:
        mox.UnsetStubs()

def test_can_get_many():
    mox = Mox()
    
    keys = ["should-be-key","should-be-key-1","should-be-key-2"]
    values = ["should-be-value","should-be-value","should-be-value"]
    
    mox.StubOutWithMock(backend,'memcache', use_mock_anything=True)
    
    cache_mock = mox.CreateMockAnything()
    cache_mock.get_multi(keys).AndReturn(values)
    
    backend.memcache.Client(["localhost:11211"]).AndReturn(cache_mock)
    
    mox.ReplayAll()
    try:
        memcache = backend.MemcachedClass(server=["localhost:11211"],timeout=30)
        assert memcache.get_many(keys) == values
        
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()    
                
def test_can_be_close():
    mox = Mox()
    
    mox.StubOutWithMock(backend,'memcache', use_mock_anything=True)
    
    cache_mock = mox.CreateMockAnything()
    cache_mock.disconnect_all()
    
    backend.memcache.Client(["localhost:11211"]).AndReturn(cache_mock)
    
    mox.ReplayAll()
    try:
        memcache = backend.MemcachedClass(server=["localhost:11211"],timeout=30)
        memcache.close()
        
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()
