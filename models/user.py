# coding: utf-8
#!/usr/bin/env python

from google.appengine.ext import db

class User(db.Model):
    lastName = db.StringProperty()
    firstName = db.StringProperty()
    username = db.StringProperty()
    created = db.DateTimeProperty()
    last_login = db.DateTimeProperty(auto_now_add=True)
    password = db.StringProperty()