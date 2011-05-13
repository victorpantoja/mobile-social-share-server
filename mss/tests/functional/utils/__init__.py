# coding: utf-8
#!/usr/bin/env python
from mss.models.user import User
from datetime import datetime
from mss.core.cache.util import get_cache
from mss.models.friendship import Friendship

def create_logged_user(last_name = 'should-be-last-name-1', first_name = 'test_create_friendship-1',  username = 'should-be-username-1'):

    user = User()
    user.last_name = last_name
    user.first_name = first_name
    user.username = username
    user.created = datetime.now()
    user.last_login = datetime.now()
    user.password = 'should-be-password'
    user.save()
    
    cache = get_cache()
    cache.set('should-be-user-auth', username)

    return user

def create_user(last_name = 'should-be-last-name-1', first_name = 'test_create_user-1',  username = 'should-be-username-1'):

    user = User()
    user.last_name = last_name
    user.first_name = first_name
    user.username = username
    user.created = datetime.now()
    user.last_login = datetime.now()
    user.password = 'should-be-password'
    user.save()

    return user

def create_friendship(user, friend):
    friendship = Friendship()
    friendship.user_id = user.id
    friendship.friend_id = friend.id
    friendship.created_dt = datetime.now()
    friendship.save()
    
    return friendship