# coding: utf-8
#!/usr/bin/env python

from mss.core.meta import get_session
from mss.models.user import User
from datetime import datetime


def test_user_can_be_saved():

    session = get_session()

    user = User()

    user.last_name = 'should-be-last-name'
    user.first_name = 'should-be-first-name'
    user.username = 'should-be-username'
    user.created = datetime.now()
    user.last_login = datetime.now()
    user.password = 'should-be-last-name'
    user.gender = 'M'
    user.email = 'should-be-email'
    user.is_staff = False
    user.is_superuser = False
    user.is_active = True
    user.save()

    user_db = session.query(User).filter(User.username == 'should-be-username').first()

    assert user_db.username == user.username

    user_db.delete()
