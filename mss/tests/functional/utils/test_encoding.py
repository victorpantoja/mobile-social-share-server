# -*- coding: utf-8 -*-

from mss.utils.encoding import smart_unicode, force_unicode, smart_str

#def test_can_smart_encode():
#    assert smart_unicode('acentuação') == 'acentuação'

def test_can_smart_encode_numbers():
    assert smart_unicode(9888,strings_only=True) == 9888

def test_can_force_unicode():
    assert force_unicode('acentuação')

def test_can_smart_str():
    assert smart_str('acentuação') == 'acentuação'

def test_can_smart_str_numbers():
    assert smart_str(9888) == '9888'

def test_can_smart_str_only():
    assert smart_str(9888,strings_only=True) == 9888
    

