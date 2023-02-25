from flask import g,Flask,render_template,request ,redirect ,url_for , flash, jsonify,abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session

from database_setup import Restaurant, Base, MenuItem,User
#fron flask.ext.httpauth import HTTPBasicAuth 

engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine
DBSession =sessionmaker(bind=engine)
session = DBSession()

app=Flask(__name__)

# auth = HTTPBasicAuth()

# @auth.verify_password
# def verify_password(username,password):
#     user=session.query(User).filter_by(username=username).one_or_none()
#     if not (user or user.verify_password(password)):
#         return False
#     g.user=user
#     return True





@app.route('/')
@app.route('/restaurants/<user>')
def homePage(user=False):
    restaurants=session.query(Restaurant).all()
    return render_template('restaurants.html',restaurants=restaurants,user=user)

@app.route('/sign-up',methods=["GET","POST"])
def sign_up():
    
    if request.method=="GET":
        return render_template('sign_up.html')
    if request.method=="POST":
        email=body=request.form["email"]
        user_exists=session.query(User).filter_by(email=email).one_or_none()
        if user_exists:
            abort(400)
        email=request.form.get("email")
        password=request.form.get("password")
        print(email,password)
        user=User(email=email)
        user.hash_password(password)
        session.add(user)
        session.commit()
        return redirect(url_for("login"))



    
    

@app.route('/login' , methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    if request.method == "POST":
        email=request.form["email"]
        password=request.form["password"]
        user=session.query(User).filter_by(email=email).one_or_none()
        if user is None:
            abort(404)
        if user.verify_password(password):
            res = make_response(expression)
            res.set_cookie('user', user.password_hash)
            return res
            
            return redirect(url_for('homePage',user=user.format()))



@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    items=session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('index.html', restaurant=restaurant, items=items )



@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/')
def Menu_Item(restaurant_id,menu_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    items=session.query(MenuItem).filter_by(restaurant_id=restaurant_id).filter_by(id=menu_id).one()
    output=items.name
    return f'{output}<br>{items.description}'


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def new_item(restaurant_id):
    if request.method == 'POST':

        newMenuItem= MenuItem(name=request.form["name"], description=request.form["description"],price=request.form["price"], course=request.form["course"] , restaurant_id=restaurant_id)
        session.add(newMenuItem)
        session.commit()
        flash('New Menu Item Created!')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id )


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',methods=['GET','POST'])
def edit_item(restaurant_id,menu_id):
    item=session.query(MenuItem).filter_by(restaurant_id=restaurant_id,id=menu_id).one()
    if request.method == 'POST':
        if item:
            item.name=request.form["name"]
            item.description=request.form["description"]
            item.price=request.form["price"]
            item.course=request.form["course"]
            session.add(item)
            session.commit()
            flash('Menu Item Edited!')
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html',restaurant_id=restaurant_id,item=item)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
def delete_item(restaurant_id,menu_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    item= session.query(MenuItem).filter_by(restaurant_id=restaurant.id,id=menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Menu Item  Deleted!')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html',restaurant_id=restaurant_id,item=item)

@app.route('/restaurants/new' , methods=['GET','POST'])
def new_restaurant():
    if request.method=='POST':
        restaurant=Restaurant(name=request.form["name"])
        session.add(restaurant)
        session.commit()
        flash('New Restaurant Created!')
        return redirect(url_for('homePage'))
    else:
        return render_template('newrestaurants.html')


@app.route('/restaurants/<int:restaurant_id>/edit' , methods=['GET','POST'])
def edit_restaurant(restaurant_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if restaurant:
            restaurant.name=request.form["name"]
            session.add(restaurant)
            session.commit()
            flash('Restaurant Edited!')
            return redirect(url_for('homePage'))
    else:
        return render_template('editrestaurant.html',restaurant=restaurant,restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/delete' , methods=['GET','POST'])
def delete_restaurant(restaurant_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if restaurant:
            session.delete(restaurant)
            session.commit()
            flash('Restaurant Deleted!')
            return redirect(url_for('homePage'))
    else:
        return render_template('deleterestaurant.html',restaurant=restaurant,restaurant_id=restaurant_id)


@app.route('/restaurants/search/' , methods=['POST'])
def search_result():
    restaurants=session.query(Restaurant).all()
    search_key =request.form['search']
    tank=0
    for restaurant in restaurants:
        if ((search_key).lower() in ((restaurant.name).lower())):
            tank+=1
    if tank==0:
        flash('No match found!')
        return redirect(url_for('homePage'))
    return render_template('searchresult.html', restaurants=restaurants,search_key=search_key) 
    
          
@app.route('/restaurants/<int:restaurant_id>/menu_items/json',methods=['GET'])
def allMenuJson(restaurant_id):
    menu_items=session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(
        menu_items=[item.format() for item in menu_items]
    )

        







if __name__=='__main__':
    app.secret_key='secret key'
    app.debug=True
    app.run() 