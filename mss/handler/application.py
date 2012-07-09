# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler, authenticated, auth_application
from mss.models.application import Application
from mss.models.application_context import ApplicationContext
from mss.models.context_type import ContextType

import hashlib
import logging
import simplejson


class ApplicationHandler(BaseHandler):
    
    @authenticated
    def applications(self, **kw):
        request_handler = kw.get('request_handler')
        
        apps = Application.all()
        
        app_list = [app.as_dict() for app in apps]
        
        return self.render_to_json({'applications': app_list}, request_handler)
    
    def create(self, **kw):
        request_handler = kw.get('request_handler')
        
        app = Application()
        app.name = request_handler.get_argument('name')
        app.icon = request_handler.get_argument('icon')
        app.callback_url = request_handler.get_argument('callback_url')
        
        m = hashlib.md5()
        m.update(app.name + app.icon)
        
        app.token = m.hexdigest()
        try:
            app.save()
        except Exception, e:
            logging.exception(e);
            return self.render_to_json({'status': 'error', 'msg': 'Application already exists.'}, request_handler)
        
        return self.render_to_json({'status': 'ok', 'msg': app.token}, request_handler)
    
    @auth_application
    def remove(self, application, **kw):
        request_handler = kw.get('request_handler')
        
        try:
            application.delete()
        except Exception, e:
            logging.exception(e);
            return self.render_to_json({'status': 'error', 'msg': 'Application not removed.'}, request_handler)
        
        return self.render_to_json({'status': 'ok', 'msg': 'You have been unsusbcribed succesfuly.'}, request_handler)
    
    @auth_application
    def subscribe(self, application, **kw):
        request_handler = kw.get('request_handler')
        
        if not request_handler.request.body:
            return self.render_to_json({'status': 'error', 'msg': "No context specified."}, request_handler)
        
        contexts = simplejson.loads(request_handler.request.body)
                
        for context in contexts['context']:
            context_type = ContextType().get_by(description=context)
            
            if context_type:
                application_context = ApplicationContext()
                application_context.application = application
                application_context.context_type = context_type
                application_context.save()
            else:
                return self.render_to_json({'status': 'error', 'msg': "Context Not Subscribed. Invalid context-type."}, request_handler)
        
        return self.render_to_json({'status': 'ok', 'msg': 'You have subscribed succesfuly.'}, request_handler)
    
    @auth_application
    def unsubscribe(self, application, **kw):
        request_handler = kw.get('request_handler')
        
        try:
            pass
        except Exception, e:
            logging.exception(e);
            return self.render_to_json({'status': 'error', 'msg': 'You have not unsubscribed!'}, request_handler)
        
        return self.render_to_json({'status': 'ok', 'msg': 'You have unsubscribed succesfuly.'}, request_handler)