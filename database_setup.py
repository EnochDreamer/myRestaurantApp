import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship 
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base= declarative_base()

class User(Base):
    __tablename__='user'
    id=Column(Integer,primary_key=True)
    email=Column(String(30),nullable=False)
    admin=Column(Integer,nullable=False,default=0)
    password_hash=Column(String(64))
    def hash_password(self,password):
        self.password_hash=pwd_context.encrypt(password)
    def verify_password(self,password):
        return pwd_context.verify(password , self.password_hash)
    def format(self):
        return(
            {
                "id":self.id,
                "email":self.email,
                "admin":self.admin
            })

class Restaurant(Base):
    __tablename__='restaurant'
    name=Column(String(80), nullable=False)
    id=Column(Integer, primary_key=True)



class MenuItem(Base):
    __tablename__= 'menu_item'
    name=Column(String(80),nullable=False)
    id=Column(Integer, primary_key=True)
    course=Column(String(250))
    description=Column(String(250))
    price= Column(String(8))
    restaurant_id=Column(Integer, ForeignKey('restaurant.id'))
    restaurant=relationship(Restaurant)
    def format(self):
        return {
            "id":self.id,
            "name":self.name,
            "course":self.course,
            "description":self.description,
            "price":self.price
        }

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
