from flask import g,Flask,render_template,request ,redirect ,url_for , flash, jsonify,abort
from sqlalchemy import create_engine
from database_setup import db_setup
from database_setup import Restaurant, MenuItem,User
from flask_httpauth import HTTPBasicAuth 
from ast import literal_eval
from flask_migrate import Migrate


app=Flask(__name__)
db=db_setup(app,Migrate)

auth = HTTPBasicAuth()


#app.template_filter('email')
# def show_email(value):
#     if value is False:
#         return value
#     elif value:
#         return eval(value)["email"]
# def isAdmin(value):
#     if value is False:
#         return value
#     if value is False:
#         return False
#     elif value:
#         print(value)
#         return eval(value)["admin"]

# app.jinja_env.filters['email'] = show_email
# app.jinja_env.filters['admin'] = isAdmin



@auth.verify_password
def verify_password(email,password):
    user=db.session.query(User).filter_by(email=email).one_or_none()
    if user is None:
        print("User not found")
        return False
    if not (user.verify_password(password)):
        return False
    elif (user.verify_password(password)):
        print(int(user.id))
        g.user_id=int(user.id)
        return True



@app.route('/')
@app.route('/restaurants/<int:user_id>')
def homePage(user_id=None):
    print(" user_id type is",type(user_id))
    restaurants=db.session.query(Restaurant).all()
    if user_id:
        user=db.session.query(User).filter_by(id=user_id).one()
        return render_template('restaurants.html',restaurants=restaurants,user=user)
    else:
        return render_template('restaurants.html',restaurants=restaurants,user=None)
    
    

@app.route('/restaurants/sign-up',methods=["GET","POST"])
def sign_up():
    if request.method=="GET":
        return render_template('sign_up.html')
    if request.method=="POST":
        email=request.form["email"]
        user_exists=db.session.query(User).filter_by(email=email).one_or_none()
        if user_exists:
            abort(400)
        password=request.form.get("password")
        image=request.files['file']
        
        print(email,password)
        user=User(email=email)
        user.hash_password(password)
        if image:
            user.save_image(image)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))

    


@app.route('/login' , methods=["GET","POST"])
@auth.login_required
def login():
    # if request.method == "GET":
    #     return render_template('login.html')
    
    # email=request.form["username"]
    # password=request.form["password"]
    # user=db.session.query(User).filter_by(email=email).one_or_none()
    # if user is None:
    #     abort(404)
    # if not (user.verify_password(password)):
    #     abort(401) 
    return redirect(url_for('homePage',user_id=g.user_id))



@app.route('/restaurants/<int:restaurant_id>/<int:user_id>/',methods=["GET"])
def restaurantMenu(restaurant_id,user_id):
    restaurant=db.session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
    user=db.session.query(User).filter_by(id=user_id).one_or_none()
    return render_template('index.html', restaurant=restaurant,user=user)



@app.route('/restaurants/<int:restaurant_id>/')
def public_menu_item(restaurant_id):
    restaurant=db.session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
    return render_template('public_menu_item.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
@auth.login_required
def new_item(restaurant_id):
    if request.method == 'POST':

        newMenuItem= MenuItem(name=request.form["name"], description=request.form["description"],price=request.form["price"], course=request.form["course"] , restaurant_id=restaurant_id)
        db.session.add(newMenuItem)
        db.session.commit()
        flash('New Menu Item Created!')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id,user_id=g.user_id))
    else:
        user=db.session.query(User).filter_by(id=g.user_id).one()
        restaurant=db.session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
        if ((restaurant.user== user) or  (user.admin)):
            return render_template('newmenuitem.html', restaurant_id=restaurant_id,user=user)
        else:
            abort(403)
    
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',methods=['GET','POST'])
@auth.login_required
def edit_item(restaurant_id,menu_id):
    item=db.session.query(MenuItem).filter_by(restaurant_id=restaurant_id,id=menu_id).one_or_none()
    if item is None:
        abort(404)
    if request.method == 'POST':
        if item:
            item.name=request.form["name"]
            item.description=request.form["description"]
            item.price=request.form["price"]
            item.course=request.form["course"]
            db.session.add(item)
            db.session.commit()
            flash('Menu Item Edited!')
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id ,user_id=g.user_id))
    else:
        user=db.session.query(User).filter_by(id=g.user_id).one()
        restaurant=db.session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
        if ((restaurant.user== user) or  (user.admin)):
            return render_template('editmenuitem.html',restaurant_id=restaurant_id,item=item,user=user)
        else:
            abort(403)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
@auth.login_required
def delete_item(restaurant_id,menu_id):
    item= db.session.query(MenuItem).filter_by(restaurant_id=restaurant_id,id=menu_id).one_or_none()
    if item is None:
        abort(404)
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        flash('Menu Item  Deleted!')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id,user_id=g.user_id))
    else:
        user=db.session.query(User).filter_by(id=g.user_id).one()
        restaurant=db.session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
        if ((restaurant.user== user) or  (user.admin)):
            return render_template('deletemenuitem.html',restaurant_id=restaurant_id,item=item,user=user)
        else:
            abort(403)
@app.route('/restaurants/new' , methods=['GET','POST'])
@auth.login_required
def new_restaurant():
    if request.method=='POST':
        restaurant=Restaurant(name=request.form["name"])
        restaurant.user_id=(g.user_id)
        db.session.add(restaurant)
        db.session.commit()
        flash('New Restaurant Created!')
        return redirect(url_for('homePage',user_id=g.user_id))
    else:
        user=db.session.query(User).filter_by(id=g.user_id).one()
        return render_template('newrestaurants.html',user=user)


@app.route('/restaurants/<int:restaurant_id>/edit' , methods=['GET','POST'])
@auth.login_required
def edit_restaurant(restaurant_id):
    restaurant=db.session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
    if restaurant is None:
        abort(404)
    if request.method == 'POST':
        if restaurant:
            restaurant.name=request.form["name"]
            db.session.add(restaurant)
            db.session.commit()
            flash('Restaurant Edited!')
            return redirect(url_for('homePage',user_id=g.user_id))
    else:
        user=db.session.query(User).filter_by(id=g.user_id).one()
        if ((restaurant.user== user) or  (user.admin)):
            return render_template('editrestaurant.html',restaurant=restaurant,restaurant_id=restaurant_id,user=user)
        else: 
            abort (403)
        


@app.route('/restaurants/<int:restaurant_id>/delete' , methods=['GET','POST'])
@auth.login_required
def delete_restaurant(restaurant_id):
    restaurant=db.session.query(Restaurant).filter_by(id=restaurant_id).one_or_none()
    if restaurant is None:
        abort(404)
    if request.method == 'POST':
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            flash('Restaurant Deleted!')
            return redirect(url_for('homePage',user_id=g.user_id))
    else:
        user=db.session.query(User).filter_by(id=g.user_id).one()
        if ((restaurant.user== user) or  (user.admin)):
            return render_template('deleterestaurant.html',restaurant=restaurant,restaurant_id=restaurant_id,user=user)
        else: 
            abort (403)


@app.route('/restaurants/search/<int:user_id>/' , methods=['POST'])
def search_result(user_id):
    restaurants=db.session.query(Restaurant).all()
    search_key =request.form['search']
    tank=0
    for restaurant in restaurants:
        if ((search_key).lower() in ((restaurant.name).lower())):
            tank+=1
    if tank==0:
        flash('No match found!')
        if not user_id:
            return redirect(url_for('homePage'))
        user=db.session.query(User).filter_by(id=user_id).one()
        return redirect(url_for('homePage',user_id=user.id))
    if not user_id:
        return render_template('searchresult.html', restaurants=restaurants,search_key=search_key,user=None)
    user=db.session.query(User).filter_by(id=user_id).one()
    return render_template('searchresult.html', restaurants=restaurants,search_key=search_key,user=user) 
     
          
@app.route('/restaurants/<int:restaurant_id>/menu_items/json',methods=['GET'])
def allMenuJson(restaurant_id):
    menu_items=db.session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(
        menu_items=[item.format() for item in menu_items]
    )

        
@app.route('/logout')
#@auth.login_required
def logout():
    return (url_for('homePage'))






if __name__=='__main__':
    app.secret_key='secret key'
    app.debug=True
    app.run() 