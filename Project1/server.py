from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from database import Restaurant,Customer,Order,Items
from databasequeries import create_user,create_order,create_menu_item,create_restaurant,get_user,get_items,get_orders_of_customer,get_restaurant

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.secret_key = 'secret_key'

db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("home.html")


if __name__=='__main__':
    app.run(debug=True)#

