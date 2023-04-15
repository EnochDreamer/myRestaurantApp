import sys
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4

db=SQLAlchemy()

database_path='postgresql://postgres:Enochgenius7@localhost:5432/restaurant'
def db_setup(app,Migrate,database_path=database_path,db=db):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"]="jkrejkvjhkgvhvjh"
    db.app = app
    db.init_app(app)
    migrate=Migrate(app,db)
    return db

class User(db.Model):
    __tablename__='my_user'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(30),nullable=False)
    admin=db.Column(db.Boolean,nullable=False,default=False)
    password_hash=db.Column(db.String())
    restaurants=db.relationship('Restaurant', backref='user',lazy=True)
    image=db.Column(db.String(),default='static/img/profile_pics/default.png')
    def hash_password(self,password):
        self.password_hash=pwd_context.encrypt(password)
    def verify_password(self,password):
        return pwd_context.verify(password , self.password_hash)
    def format(self):

        return(
            {
                "id":self.id,
                "email":self.email,
                "admin":self.admin,
                "image":self.image
            })

    def save_image(self, file):
        """Saves an image from `request.files`"""
        _, fmt = os.path.splitext(file.filename)
        newFileName = str(uuid4()).replace('-', '') + fmt
        os.makedirs(os.path.join('static', 'img', 'profile_pics'), exist_ok=True)
        path = os.path.join("static", "img", "profile_pics", newFileName)
        print(path)
        file.save(path)
        self.image = path
        db.session.commit()




class Restaurant(db.Model):
    __tablename__='restaurant'
    name=db.Column(db.String(80), nullable=False)
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('my_user.id'), default=1)
    menu_items=db.relationship('MenuItem', backref='restaurant',lazy=True)

class MenuItem(db.Model):
    __tablename__= 'menu_item'
    name=db.Column(db.String(80),nullable=False)
    id=db.Column(db.Integer, primary_key=True)
    course=db.Column(db.String())
    description=db.Column(db.String())
    price= db.Column(db.String(8))
    restaurant_id=db.Column(db.Integer, db.ForeignKey('restaurant.id'), default=1)
    
    def format(self):
        return {
            "id":self.id,
            "name":self.name,
            "course":self.course,
            "description":self.description,
            "price":self.price
        }


