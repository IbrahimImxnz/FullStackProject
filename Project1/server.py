from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SECRET_KEY"] = "mysecretkey"

db = SQLAlchemy(app)

from .database import Customer, Restaurant, Order, Items, Menu
