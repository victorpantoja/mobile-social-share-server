# coding: utf-8
#!/usr/bin/env python
from mss.models.user import User
from datetime import datetime
from mss.core.cache.util import get_cache
from mss.models.friendship import Friendship
from mss.models.invite import Invite
from mss.models.network import Network

import hashlib
from mss.models.invite_email import InviteEmail

def create_logged_user(last_name = 'should-be-last-name-1', first_name = 'test_create_user',  username = 'should-be-username-1'):

    user = User()
    user.last_name = last_name
    user.first_name = first_name
    user.username = username
    user.gender = User._MALE
    user.created = datetime.now()
    user.last_login = datetime.now()
    
    password = 'should-be-password'
    
    m = hashlib.md5()
    m.update(password)
    
    user.password = m.hexdigest()
    user.save()
    
    cache = get_cache()
    cache.set('should-be-user-auth', username)

    return user

def create_user(last_name = 'should-be-last-name-1', first_name = 'test_create_user-1',  username = 'should-be-username-1'):

    user = User()
    user.last_name = last_name
    user.first_name = first_name
    user.username = username
    user.gender = User._MALE
    user.created = datetime.now()
    user.last_login = datetime.now()

    password = 'should-be-password'
    
    m = hashlib.md5()
    m.update(password)
    
    user.password = m.hexdigest()

    user.save()

    return user

def create_friendship(user, friend):
    friendship = Friendship()
    friendship.user_id = user.id
    friendship.friend_id = friend.id
    friendship.created_dt = datetime.now()
    friendship.save()
    
    return friendship

def create_invite(user, friend):
    invite = Invite()
    invite.user_id = user.id
    invite.friend_id = friend.id
    invite.date = datetime.now()
    invite.save()
    
    return invite

def create_network(name = 'should-be-network-name', icon = 'should-be-network-icon', available = True):
    network = Network()
    network.name = name
    network.icon = icon
    network.availabe = available
    network.save()
    
    return network

def create_invite_email(user,email):
    
    invite_email = InviteEmail()
    invite_email.user_id = user.id
    
    m = hashlib.md5()
    m.update("%s%s" % (email,user.id))

    code = m.hexdigest()
    
    invite_email.code = code
    invite_email.date = datetime.now()
    invite_email.save()
    
    return invite_email