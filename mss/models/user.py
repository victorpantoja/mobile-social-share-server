# coding: utf-8
#!/usr/bin/env python

from mss.core import meta
from mss.models.base import Model, Repository
from sqlalchemy import Column, String, DateTime, Integer
from mss.core.cache.util import cached, CachedExtension


class UserRepository(Repository):
    
    @staticmethod
    @cached
    def get_by(username):
        session = meta.get_session()  
        user_db = session.query(User).filter(User.username==username).first()

        return user_db

class User(Model, UserRepository):
    
    __mapper_args__ = {'extension': CachedExtension()}
    
    _FEMALE = 'F'
    _MALE = 'M'
    _OTHER = 'O'
    
    __tablename__ = 'users'
        
    id = Column('user_id', Integer, primary_key=True)
    last_name = Column('lastname_txt', String)
    first_name = Column('firstname_txt', String)
    username = Column('username_txt', String)
    gender = Column('gender_flg', String)
    created = Column('criate_dt', DateTime)
    last_login = Column('lastlogin_dt', DateTime)
    password = Column('password_txt', String)