from flask import Flask, render_template, redirect, url_for, request,flash,session
from flask_sqlalchemy import SQLAlchemy
from database import Restaurant,Customer,Order,Items,db
from databasequeries import create_user,create_order,create_menu_item,create_restaurant,get_user,get_items,get_orders_of_customer,get_restaurant
import re
from werkzeug.security import check_password_hash,generate_password_hash


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
        
        create_user(email,firstname,lastname,address,password,zip)
        flash("Account successfully created!")
        return redirect(url_for("home"))
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
        create_restaurant(name,email,address,password,image,description,deliveryradius,openinghrs)
        flash("Account successfully created!")
        return redirect(url_for("home"))
    return render_template("registrest.html")

@app.route("/login/user", methods=['GET','POST'])
def user_login():
    if request.method == "POST":
        email = request.form.get("Email")
        password = request.form.get("Password")

        user = get_user(email)
        if user and user.check(password):
            session["user_id"]=user.C_id
            flash("Login successful")
            return redirect(url_for("home"))
        else:
            flash("Wrong email or password")
            return redirect(url_for("user_login"))
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
            return redirect(url_for("home"))
        else:
            flash("Wrong email or password")
            return redirect(url_for("user_login"))
    return render_template("restlogin.html")




with app.app_context():
    db.create_all()

if __name__=='__main__':
    app.run(debug=True)

