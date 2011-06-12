# coding: utf-8
#!/usr/bin/env python

from mss.models.base import Model, Repository
from sqlalchemy import Column, String, DateTime, Integer


class UserRepository(Repository):
    pass

class User(Model, UserRepository):
    
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