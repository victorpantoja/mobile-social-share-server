# coding: utf-8
#!/usr/bin/env python

import logging
import simplejson

from mss.utils import Singleton
from mss.utils.beanstalkhelper import BeanstalkHelper


class ContextQueue(Singleton):

    def add(self, application, context, token, callback_url):
        try:
            queue = BeanstalkHelper().getHostLocal()

            context_item = {'application': application,
                            'context': context,
                            'token': token,
                            'callback_url': callback_url}

            data = simplejson.dumps(context_item)

            logging.debug("[ContextQueue] message=%s" % data)

            queue.use("context")
            logging.debug("[ContextQueue] use=context OK")
            queue.put(data)

            logging.debug("[ContextQueue] - PUT OK %s" % data)
        except Exception:
            logging.exception("[ContextQueue] Nao foi possivel realizar o put agora")
