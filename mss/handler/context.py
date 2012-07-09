# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler, authenticated
from mss.models.application import Application
from mss.models.context_type import ContextType
from mss.models.context import Context
from mss.models.contextapplication import ContextApplication
from mss.utils.context import ContextQueue

from datetime import datetime

import simplejson


class ContextHandler(BaseHandler):

    @authenticated
    def context(self, user, **kw):
        request_handler = kw.get('request_handler')

        if not request_handler.request.body:
            return self.render_to_json({'status': 'error', 'msg': "Context Message is Empty."}, request_handler)

        data = simplejson.loads(request_handler.request.body)

        profile = user.get_profile(user_id=user.id)

        tokens = simplejson.loads(profile.tokens)

        for app_name in data['application']:
            application = Application().get_by(name=app_name)

            if application:
                #TODO - verificar se a aplicacao assina o contexto
                for description in data['context'].keys():
                    context_type = ContextType().get_by(description=description)

                    if context_type:
                        context = Context()
                        context.user_id = user.id
                        context.context_type_id = context_type.id
                        context.context = data['context'][description]
                        context.updated = datetime.now()
                        context.save()

                        context_application = ContextApplication()
                        context_application.application = application
                        context_application.context = context
                        context_application.save()
                    else:
                        return self.render_to_json({'status': 'error', 'msg': "Context Not Sent. Invalid context-type."}, request_handler)

                ContextQueue().add(application.name, data['context'], tokens[app_name], application.callback_url)
            else:
                return self.render_to_json({'status': 'error', 'msg': "Context Not Sent. Application not registered."}, request_handler)

        return self.render_to_json({'status': 'ok', 'msg': "Context Sent."}, request_handler)

    def callback(self, **kw):
        request_handler = kw.get('request_handler')

        return self.render_to_json({'status': 'ok', 'msg': "Context Received."}, request_handler)
