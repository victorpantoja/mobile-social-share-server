# coding: utf-8
#!/usr/bin/env python

from mss.models.base import Model, Repository
from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relation
from mss.models.user import User


class FriendshipRepository(Repository):
    pass

class Friendship(Model, FriendshipRepository):
    
    __tablename__ = 'friendship'
        
    id = Column('friendship_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey("users.user_id"))
    friend_id = Column('friend_id', Integer, ForeignKey("users.user_id"))
    created_dt = Column('created_dt', DateTime)

    user = relation(User, primaryjoin=user_id == User.id)