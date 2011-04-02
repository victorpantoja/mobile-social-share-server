# coding: utf-8
#!/usr/bin/env python

from tornado.web import RequestHandler
from mako.template import Template
from mako.lookup import TemplateLookup
from tornado.options import options

import simplejson

class BaseHandler(RequestHandler):
    def __init__(self, application, request, transforms=None):
        RequestHandler.__init__(self, application, request)
        self.lookup = TemplateLookup(directories=[options.template_dir], output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'])

    def render_template(self,template_name, **kwargs):
        new_template = self.lookup.get_template(template_name)
        self.write(new_template.render(**kwargs))
    
    def render_to_template(self, template, **kw):
        lookup = TemplateLookup(directories=[options.template_dir], 
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
        
    def render_error(self, message="Ops! Ocorreu um erro!"):
        return self.render_to_json({"errors":{"error":{"message": message}}})

    def render_success(self, message="Operação realizada com sucesso!"):
        return self.render_to_json({"errors":"", "message":message})
    
    def render_to_json(self, data):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return simplejson.dumps(data)