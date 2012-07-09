# coding: utf-8
#!/usr/bin/env python

import logging

from mss.core import settings
from mss.core.cache import get_cache
from mss.models.user import User
from mss.models.application import Application

from mako import exceptions
from mako.lookup import TemplateLookup

import simplejson


class BaseHandler():

    def render_to_template(self, template, **kw):
        lookup = TemplateLookup(directories=settings.TEMPLATE_DIRS,
                                output_encoding='utf-8',
                                input_encoding='utf-8',
                                default_filters=['decode.utf8'])
        try:
            template = lookup.get_template(template)

            return template.render(**kw)
        except Exception, e:
            if settings.DEBUG:
                return exceptions.html_error_template().render()
            else:
                logging.exception("Erro ao renderizar o template!")
                raise e

    def render_error(self, message="Ops! Ocorreu um erro!", handler=None):
        return self.render_to_json({"errors":{"error":{"message": message}}}, handler)

    def render_success(self, message="Operação realizada com sucesso!", handler=None):
        return self.render_to_json({"errors":"", "message":message}, handler)
    
    def render_to_json(self, data, handler):
        handler.set_header("Content-Type", "application/json; charset=UTF-8")
        return simplejson.dumps(data)

    def render_to_text(self, data, handler):
        handler.set_header("Content-Type", "text/plain; charset=UTF-8")
        return data


def authenticated(fn):
    def authenticated_fn(self, *args, **kw):
        request_handler = kw.get('request_handler')    

        cache = get_cache()

        username = cache.get(kw.get('auth'))

        if not username:
            return self.render_to_json({'status': 'error', 'msg': 'User not authenticated.'}, request_handler)
        else:
            user = User().get_by(username=username)

            if not user:
                return self.render_to_json({'status': 'error', 'msg': 'User not authenticated.'}, request_handler)

        return fn(self, user=user, *args, **kw)

    return authenticated_fn

def auth_application(fn):
    def authenticated_fn(self, *args, **kw):
        request_handler = kw.get('request_handler')    

        application = Application().get_by_token(token=kw.get('token'))

        if not application:
            return self.render_to_json({'status': 'error', 'msg': 'Invalid Token or Application.'}, request_handler)

        return fn(self, application=application, *args, **kw)

    return authenticated_fn