# coding: utf-8
#!/usr/bin/env python

from mss.models.base import Model, Repository
from mss.models.user import User
from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relation


class FriendshipRepository(Repository):
    """
        Classe de Acesso ao Banco
    """
    pass


class Friendship(Model, FriendshipRepository):
    """
        Modelo da Relação entre Usuários (Amizade)
    """

    __tablename__ = 'friendship'

    id = Column('friendship_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey("auth_user.id"))
    friend_id = Column('friend_id', Integer, ForeignKey("auth_user.id"))
    created_dt = Column('created_dt', DateTime)

    friend = relation(User, primaryjoin=friend_id == User.id)
