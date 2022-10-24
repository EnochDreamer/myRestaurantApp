from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
'''restaurant=session.query(Restaurant).all()
for r in restaurant:
    print(r.id,r.name)'''

'''items=session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
for item in items:
   print(item.name)'''


'''vburgers= session.query(MenuItem).filter_by(name='Veggie Burger')
for vburger in vburgers:
    print(vburger.id)
    print(vburger.price)
    print(vburger.restaurant.name)
    print("\n")'''

'''urbanvburger= session.query(MenuItem).filter_by(id=8).one()
urbanvburger.price='$2.99'
session.add(urbanvburger)
session.commit()'''
  
'''vburgers= session.query(MenuItem).filter_by(name='Veggie Burger')
for vburger in vburgers:
    if vburger.price != '$2.99':
        vburger.price='$2.99'
        session.add(vburger)
        session.commit()'''
'''restaurant_id=2
restaurant=session.query(Restaurant).all()
items=session.query(MenuItem).all()
output=0
for item in items:
    output=f'{item.id}\n </br>\n {item.name}\n </br>\n {item.price}\n </br>\n {item.course}'   
     
    print( output)'''
'''restaurant_id,menu_id=1,1
restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
item= session.query(MenuItem).filter_by(restaurant_id=restaurant.id).filter_by(id=menu_id).one()
print(item)

def search_result():
    if request.method=='POST':
        restaurant=session.query(Restaurant).filter_by(name=request.form.get(('search')).title()).one()
        return render_template('searchresult.html',restaurant=restaurant)
    else:
        return redirect(url_for('homePage'))'''

restaurants=session.query(Restaurant).all()
input='E'
for restaurant in restaurants:
    print((input).lower() not in ((restaurant.name).lower()))


