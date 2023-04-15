from flask_sqlalchemy import SQLAlchemy
from database_setup import User ,Restaurant,db_setup
from flask_migrate import Migrate
from project import app
db=db_setup(app,Migrate)

user=db.session.query(User).filter_by(email='enochekele5@gmail.com').first()
restaurant=db.session.query(Restaurant).filter_by(id=2).first()

user.admin=1
#restaurant.user_id=1
db.session.add(user)
#db.session.add(restaurant)
db.session.commit()

# print(user.format())
# print(((user.restaurants)[1]).name)
# print(restaurant.user.email)
