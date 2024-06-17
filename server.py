from flask import Flask, render_template, redirect, url_for, request,flash,session, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from database import Restaurant,Customer,Order,Items,db
from databasequeries import get_orders_of_restaurant,create_user,create_order,create_menu_item,create_restaurant,get_user,get_items,get_orders_of_customer,get_restaurant,delete_item
import re
import datetime
import smtplib
import string
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.secret_key = 'secret_key'

db.init_app(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register/user", methods=['GET','POST'])
def register_user():
    if request.method == "POST":
        email=request.form.get("Email")
        firstname=request.form.get("First_Name")
        lastname=request.form.get("Last_Name")
        address=request.form.get("Address")
        zip=request.form.get("Zip")
        password=request.form.get("Password")
        confirmpassword=request.form.get("Confirmed_Password")

        if password != confirmpassword:
            flash("Passwords do not match")
            return redirect(url_for("register_user"))
        
        if get_user(email):
            flash("Email already exists!")
            return redirect(url_for("register_user"))
        
        if not re.match(r"\d{5}",zip):
            flash("Zip must be a 5 digit number please")
            return redirect(url_for("register_user"))
        
        create_user(email,firstname,lastname,address,password,zip)
        flash("Account successfully created!")
        return redirect(url_for("userhome"))
    return render_template("registuser.html")

@app.route("/register/restaurant", methods=['GET','POST'])
def register_restaurant():
    if request.method == "POST":
        name=request.form.get("Name")
        email=request.form.get("Email")
        address=request.form.get("Address")
        image=request.form.get("image")
        description=request.form.get("Description")
        deliveryradius_start=request.form.get("Delivery_radius_start")
        deliveryradius_end=request.form.get("Delivery_radius_end")
        openinghrs=request.form.get("Opening_hours")
        password=request.form.get("Password")
        confirmpassword=request.form.get("Confirmed_Password")

        if password != confirmpassword:
            flash("Passwords do not match")
            return redirect(url_for("register_restaurant"))
        
        if get_restaurant(email):
            flash("Email already exists!")
            return redirect(url_for("register_restaurant"))
        
        if not re.match(r"^\d{5}$", deliveryradius_start) or not re.match(r"^\d{5}$", deliveryradius_end):
            flash("Radius must be in zip code format, i.e. 5 digits only")
            return redirect(url_for("register_restaurant"))
        
        if not re.match(r"\d{1,2}\D\D-\d{1,2}\D\D", openinghrs):
            flash("please insert correct format for opening hours!")
            return redirect(url_for("register_restaurant"))

        deliveryradius = f"{deliveryradius_start} until {deliveryradius_end}"
        restaurant = create_restaurant(name,email,address,password,image,description,deliveryradius,openinghrs)
        restaurant.set_deliveryradius(deliveryradius_start, deliveryradius_end)
        db.session.commit()
        flash("Account successfully created!")
        return redirect(url_for("resthome"))
    return render_template("registrest.html")

@app.route("/login/user", methods=['GET','POST'])
def user_login():
    if request.method == "POST":
        email = request.form.get("Email")
        password = request.form.get("Password")

        user = get_user(email)
        if user and user.check(password):
            session["user_id"]=user.C_id
            session["user_zip"]=user.Zip
            session["email"]=user.Email
            flash("Login successful")
            return redirect(url_for("userhome"))
        else:
            flash("Wrong email or password")
            return redirect(url_for("home"))
    return render_template("loginuser.html")
       
@app.route("/login/restaurant", methods=["GET","POST"])
def restaurant_login():
    if request.method == "POST":
        email = request.form.get("Email")
        password = request.form.get("Password")

        restaurant = get_restaurant(email)
        if restaurant and restaurant.check(password):
            session["restaurant_id"]=restaurant.R_id
            flash("Login successful")
            return redirect(url_for("resthome"))
        else:
            flash("Wrong email or password")
            return redirect(url_for("user_login"))
    return render_template("restlogin.html")

@app.route("/logout/user")
def logoutuser():
    session.pop("user_id",None)
    flash("Logged out")
    return redirect(url_for("home"))

@app.route("/logout/restaurant")
def logoutrest():
    session.pop("restaurant_id",None)
    flash("Logged out")
    return redirect(url_for("home"))

def get_restaurants(zip):
    try:
        restaurants = Restaurant.query.all()
        restaurants_in_area = []

        for i in restaurants:
            deliveryradius = i.get_deliverradius()
            if str(zip) in deliveryradius:
                restaurants_in_area.append(i)

        return restaurants_in_area 
    except Exception as e:
        print(f"Error in getting the restaurants: {e}")
        return []       

@app.route("/restaurant/home", methods = ["GET", "POST"])
def resthome():
    if "restaurant_id" not in session:
        flash("Please login first")
        return redirect(url_for("restaurant_login"))
    restaurant_id = session["restaurant_id"]
    restaurant = Restaurant.query.get(restaurant_id)
    if request.method == "POST":
        category = request.form.get("Category")
        name = request.form.get("Name")
        price = request.form.get("Price")
        description = request.form.get("Description")
        picture = request.form.get("Picture")
        total_price = price

        create_menu_item(category,name,price,description,picture,total_price,restaurant_id)
        flash("Item added to menu")
        return redirect(url_for("resthome"))
    items = get_items(restaurant_id)
    return render_template("resthome.html", restaurant=restaurant, items=items)

@app.route("/restaurant/delete_item/<int:item_id>", methods=["POST"])
def delete_menuitem(item_id):
    delete_item(item_id)
    flash("item deleted from Menu")
    return redirect(url_for("resthome"))

@app.route("/user/home")
def userhome():
    if "user_id" not in session:
        flash("Please login first!")
        return redirect(url_for("user_login"))
    zip = session.get("user_zip")
    email = session.get("email")
    user = get_user(email)
    restaurants = get_restaurants(zip)
    return render_template("userhome.html", restaurants=restaurants, user=user)

@app.route("/restaurant/<int:restaurant_id>/menu")
def viewitems(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    items = get_items(restaurant_id)
    return render_template("viewitems.html", restaurant=restaurant, items = items)

@app.route("/basket/add/<int:item_id>", methods = ["POST"])
def addtobasket(item_id):
    if "user_id" not in session:
        flash("Please login first")
        return redirect(url_for("user_login"))
    item = Items.query.get(item_id)
    restaurant_id = item.R_id
    restaurant = str(restaurant_id)

    if "basket" not in session:
        session["basket"]={}
    
    basket = session["basket"]

    if basket and list(basket.keys())[0] != restaurant:
        flash("Previous basket deleted!")
        session.pop("basket")
    
    if restaurant not in basket:
        basket[restaurant] = {}

    if str(item_id) in basket[restaurant]:
        basket[restaurant][str(item_id)] += 1
    else:
        basket[restaurant][str(item_id)] = 1

    session["basket"]=basket
    flash("item added to basket")
    return redirect(url_for("viewitems",restaurant_id=restaurant_id)) 

@app.route("/basket")
def viewbasket():
    if "user_id" not in session:
        flash("Please login first!")
        return redirect(url_for("user_login"))

    if "basket" not in session:
        flash("your basket is empty")
        return redirect(url_for("userhome"))

    basket = session["basket"]
    restaurant_id = int(list(basket.keys())[0])       
    restaurant = Restaurant.query.get(restaurant_id)
    basket_items = [(Items.query.get(int(item_id)), quantity) for item_id, quantity in basket[str(restaurant_id)].items()]
    total=0
    for item_id,quantity in basket[str(restaurant_id)].items():
        item = Items.query.get(int(item_id))
        total = item.Price * quantity
    if not list(basket_items):
        return redirect(url_for("userhome"))  
    else: 
        return render_template("basket.html", basket_items=basket_items, restaurant = restaurant, total= total)

@app.route("/basket/remove/<int:item_id>", methods=["POST"])
def removefrombasket(item_id):
    if "basket" not in session:
        flash("Your basket is empty")
        return redirect(url_for("view_basket"))
    basket = session["basket"]
    r_id = int(list(basket.keys())[0])

    item = str(item_id)
    restaurant = str(r_id)

    if item in basket[restaurant]:
        del basket[restaurant][item]

    restaurant_id = int(list(basket.keys())[0])
    basket_items = [(Items.query.get(int(item_id)), quantity) for item_id, quantity in basket[str(restaurant_id)].items()]    

    session["basket"]=basket
    flash("Item removed from basket")
    if not list(basket_items): 
        return redirect(url_for("userhome"))
    else: 
        return redirect(url_for("viewbasket"))

@app.route("/basket/checkout", methods=["POST"])
def checkout():
    if "user_id" not in session:
        flash("Please login first")
        return redirect(url_for("user_login"))
    user_id = session["user_id"]
    if "basket" not in session:
        flash("Your basket is empty")
        return redirect(url_for("userhome"))

    basket = session["basket"]
    
    r_id = int(list(basket.keys())[0])
    order = create_order("pending",datetime.datetime.now(),user_id,r_id)
    for item_id, quantity in basket[str(r_id)].items():
        item = Items.query.get(int(item_id))
        for _ in range(quantity):
            order.items.append(item)
            

    db.session.commit()
    session.pop("basket")
    flash("Order placed")
    return redirect(url_for("userhome"))

@app.route("/userhome/orders", methods = ["GET", "POST"])
def vieworders():
    if "user_id" not in session:
        flash("Please login first")
        return redirect(url_for("user_login"))
    customer = session.get("user_id")
    orders  = get_orders_of_customer(customer)
    return render_template("userorders.html",orders=orders)

@app.route("/resthome/orders", methods = ["GET","POST"])
def viewrestorders():
    if "restaurant_id" not in session:
            flash("Please login first")
            return redirect(url_for("restaurant_login")) 
    r_id = session.get("restaurant_id")
    orders = get_orders_of_restaurant(r_id)

    if request.method == "POST":
        O_id = request.form.get("O_id")
        State = request.form.get("State")
        changedorder = Order.query.get(O_id)
        if changedorder and changedorder.restaurant_id == r_id:
            changedorder.State = State
            db.session.commit()
            flash("Order status updated")
        else:
            flash("Order not found")    
        return redirect(url_for("viewrestorders"))    

    return render_template("restorders.html", orders=orders)

@app.route("/userhome/details", methods = ["POST","GET"])
def viewdetails():
    if "user_id" not in session: 
        flash("Please login first")
        return redirect(url_for("user_login"))
    
    #email = session.get("email")
    user = Customer.query.get(session.get("user_id"))

    if request.method == "POST":
        #C_id = request.form.get("C_id")
        #field = request.form.get("field")
        #new_value = request.form.get("new_value")
        Email = request.form.get("Email")
        First_Name = request.form.get("First_Name")
        Last_Name = request.form.get("Last_Name")
        Address = request.form.get("Address")
        Zip = request.form.get("Zip")
        #changeduser = Customer.query.get(C_id)

        if Email:
            user.Email = Email
        if First_Name:
            user.First_Name = First_Name
        if Last_Name:
            user.Last_Name = Last_Name
        if Address:
            user.Address = Address
        if Zip: 
            user.Zip = Zip                 
        #if changeduser:
            #changeduser.Email=Email
            #changeduser.First_Name=First_Name
            #changeduser.Last_Name=Last_Name
            #changeduser.Address=Address
            #changeduser.Zip=Zip
            #this method required to update all fields and not each one on its own
            #if field == "Email":
                #changeduser.Email = new_value
            #elif field == "First_Name":
                #changeduser.First_Name = new_value
            #elif field == "Last_Name":
                #changeduser.Last_Name = new_value
            #elif field == "Address":
                #changeduser.Address = new_value
            #elif field == "Zip":
                #changeduser.Zip = new_value
            #user = Customer.query.get(changeduser.C_id)
        db.session.commit()
        flash("Profile updated successfully")
        return redirect(url_for("viewdetails")) 
    

    return render_template("userdetails.html",user=user)   

@app.route("/login/forgotpass", methods = ["POST"])
def forgotpass():
    if request.method == "POST":
        email = request.form.get("Email")

    SMTP = {
    "gmail.com": {"server": "smtp.gmail.com", "port": 587},
    "outlook.com": {"server": "smtp.office365.com", "port": 587},
    "hotmail.com": {"server": "smtp.office365.com", "port": 587},
    }

    domain = email.split('@')[1]
    smtp_object = smtplib.SMTP(SMTP[domain]["server"],SMTP[domain]["port"])
    smtp_object.ehlo()
    smtp_object.starttls()

    

    smtp_object()



with app.app_context():
    db.create_all()

if __name__=='__main__':
    app.run(debug=True)

