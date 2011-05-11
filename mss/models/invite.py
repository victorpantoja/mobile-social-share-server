# coding: utf-8
#!/usr/bin/env python

from mss.models.base import Model, Repository
from mss.models.user import User
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relation

class InviteRepository(Repository):
    pass

class Invite(Model, InviteRepository):
    
    __tablename__ = 'invite'
    
    id = Column('invite_id', Integer, primary_key=True)   
    user_id = Column('user_id', Integer, ForeignKey("user.user_id"))
    friend_id = Column('friend_id', Integer, ForeignKey("user.user_id"))
    date = Column('invite_dt', DateTime)

    user = relation(User, primaryjoin=user_id == User.id)