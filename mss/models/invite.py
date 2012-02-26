# coding: utf-8
#!/usr/bin/env python

from mss.models.base import Model, Repository
from mss.models.user import User
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relation


class InviteRepository(Repository):
    """
        Classe de Acesso ao Banco
    """
    pass


class Invite(Model, InviteRepository):
    """
        Modelo de Convite por Sistema
    """

    __tablename__ = 'invite'

    id = Column('invite_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey("auth_user.id"))
    friend_id = Column('friend_id', Integer, ForeignKey("auth_user.id"))
    date = Column('invite_dt', DateTime)

    friend = relation(User, primaryjoin=friend_id == User.id)
    user = relation(User, primaryjoin=user_id == User.id)
