# coding: utf-8
#!/usr/bin/env python

from mox import Mox
from mss.core import cache
import hashlib

def test_can_be_get_key_from_expire():
    mox = Mox()
    
    class ShouldBeModule(object):
        def ShouldBeMethod(self, param=None):
            pass
        
        ShouldBeMethod.fn = ShouldBeMethod

    expire = "ShouldBeModule.ShouldBeMethod(should-be-params)"
    
    instance_mock = mox.CreateMockAnything()
    instance_mock.id = 101
    instance_mock.ShouldBeMethod = "should-be-method-instance"

    cached_extension = cache.CachedExtension()
    
    mox.StubOutWithMock(cached_extension, 'prepare_parameters', use_mock_anything=True)
    mox.StubOutWithMock(cached_extension, 'load_model', use_mock_anything=True)
    
    cached_extension.prepare_parameters(instance_mock, "should-be-params").AndReturn({"param":"should-be-prepare-params"})

    module_instance = ShouldBeModule()
    cached_extension.load_model('shouldbemodule', 'ShouldBeModule').AndReturn(module_instance)
    
    mox.ReplayAll()
    try:
        
        md5, key = cached_extension.get_key_from_expires(instance_mock, expire)
        assert md5 == hashlib.md5("mss.tests.unit.core.cache.test_cache.ShouldBeModule().ShouldBeMethod(param=should-be-prepare-params)").hexdigest()
         
        mox.VerifyAll()
    finally:
        mox.UnsetStubs()
