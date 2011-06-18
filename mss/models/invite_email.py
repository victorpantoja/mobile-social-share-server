# coding: utf-8
#!/usr/bin/env python

from mss.models.base import Model, Repository
from mss.models.user import User
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relation

class InviteEmailRepository(Repository):
    """
        Classe de Acesso ao Banco
    """
    pass

class InviteEmail(Model, InviteEmailRepository):
    """
        Modelo do Convite por Email
    """
        
    __tablename__ = 'invite_email'
  
    id = Column('invite_email_id', Integer, primary_key=True)   
    user_id = Column('user_id', Integer, ForeignKey("users.user_id"))
    code = Column('code_txt', String)
    date = Column('invite_dt', DateTime)

    user = relation(User)