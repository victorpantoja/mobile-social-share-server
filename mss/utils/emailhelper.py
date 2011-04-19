# coding: utf-8
#!/usr/bin/env python

import logging, smtplib, re

from monitor.core.exception import ValidarEmailException
from tornado.options import options
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class EmailHelper:

    @staticmethod
    def mensagem(destinatario=None,corpo=None,subject=None,strFrom=None):

        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject
        msgRoot['From'] = strFrom
        msgRoot['To'] = destinatario
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgText = MIMEText('This is the alternative plain text message.')
        msgAlternative.attach(msgText)

        msgText = MIMEText(corpo, 'html')
        msgAlternative.attach(msgText)

        return msgRoot.as_string()

    @staticmethod
    def enviar(mensagem=None,destinatario=None):

        sender = 'noreply@globo.com'
        receivers = []

        #suporta varios destinararios
        receivers.append(destinatario)

        server = smtplib.SMTP(options.EMAIL['server'],options.EMAIL['port'])
        server.sendmail(sender, receivers, mensagem)
        
    @staticmethod
    def validateEmail(email):
    
        if len(email) > 7:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
                return True
        raise ValidarEmailException
