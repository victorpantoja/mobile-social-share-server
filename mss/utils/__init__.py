# coding: utf-8
#!/usr/bin/env python

from random import choice, getrandbits
import string


class Singleton(object):
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


def create_random_string():
    size = 9
    return ''.join([choice(string.letters + string.digits) for i in range(size)])