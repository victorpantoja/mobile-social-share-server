# coding: utf-8
#!/usr/bin/env python

from google.appengine.ext import db

class User(db.Model):
    username = db.UserProperty()
    created = db.DateTimeProperty()
    last_login = db.DateTimeProperty()
    password = db.StringProperty()