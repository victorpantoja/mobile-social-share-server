# coding: utf-8
#!/usr/bin/env python

from routes import Mapper
from mss.rotas import rotas

__mapper__ = None
__controllers__ = None


def get_mapper():
    global __mapper__
    if not __mapper__:
        mapper = Mapper()
        for name, route, controller, action, module in rotas:
            mapper.connect(name, route, controller="%s.%s" % (module, controller), action=action)
        __mapper__ = mapper
    return __mapper__


def get_controller(controller, debug=False):
    global __controllers__
    if not __controllers__:
        __controllers__ = {}

    if not controller in __controllers__:
        module, ctrl_name = controller.split(".")
        ctrl = getattr(__import__("mss.handler.%s" % module, fromlist=[ctrl_name]), ctrl_name)
        if debug:
            return ctrl()
        else:
            __controllers__[controller] = ctrl()

    return __controllers__[controller]
