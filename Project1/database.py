from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

viewers = db.Table(
    "customer_restaurant_association",
     db.Column("customer_id", db.Integer,db.ForeignKey("C_id"),primary_key = True),
     db.Column("restaurant_id",db.Integer,db.ForeignKey("R_id"),primary_key = True)                                           
)

orders = db.Table( 
    "order_items",
    db.Column("order_id",db.Integer,db.ForeignKey("O_id"),primary_key=True),
    db.Column("item_id",db.Integer,db.ForeignKey("I_id"),primary_key=True)
)

class Restaurant(db.Model):
    R_id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), unique=True, nullable = False)
    Address = db.Column(db.String(100), nullable=False)
    Password = db.Column(db.String(128), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    Description = db.Column(db.String(1000), nullable=False)
    Delivery_radius = db.Column(db.Integer, nullable = False)
    Opening_hours = db.Column(db.String(255), nullable = False)
    customers = db.relationship("Customer",secondary = viewers, backref = db.backref("'viewed_restaurants', lazy=True"))
    menu = db.relationship("Menu", backref="Restaurant" ,uselist = False)
    orders = db.relationship("Order",backref="Restaurant",lazy=True)

class Customer(db.Model):
    C_id = db.Column(db.Integer, primary_key = True)
    First_Name = db.Column(db.String(50), nullable = False)
    Last_Name = db.Column(db.String(50), nullable = False)
    Address = db.Column(db.String(100), nullable=False)
    Password = db.Column(db.String(128), nullable=False)
    Zip = db.Column(db.Integer, nullable = False) 
    restaurants = db.relationship("Restaurant",secondary = viewers, backref = db.backref("'viewers', lazy=True"))
    orders = db.relationship("Order",backref="Customer",lazy=True)

class Menu(db.Model):
    M_id = db.Column(db.Integer, primary_key = True)
    R_id = db.Column(db.Integer, db.ForeignKey("R_id"))
    items = db.relationship("Items",backref="Menu",lazy=True)

class Items(db.Model):
    I_id = db.Column(db.Integer, primary_key = True)
    Category = db.Column(db.String(50), nullable = False)    
    Name = db.Column(db.String(50), nullable = False)
    Price = db.Column(db.Integer, nullable = False)
    Description = db.Column(db.String(1000), nullable = False)
    Picture = db.Column(db.String(255), nullable = True)
    Total_price = db.Column(db.Integer, nullable = False)
    menu_id = db.Column(db.Integer, db.ForeignKey("M_id"))
    restaurant = db.relationship("Restaurant",backref="Items",secondary="Menu")
    orders = db.relationship("Order",secondary=orders,backref="Items") 

class Order(db.Model):
    O_id = db.Column(db.Integer,primary_key = True)
    State = db.Column(db.String(50),nullable = False)
    Date = db.Column(db.String(255), nullable = False)
    customer_id = db.Column(db.Integer,db.ForeginKey("C_id"))
    items = db.relationship("Items",secondary=orders,backref="Order")
    restaurant_id = db.Column(db.Integer,db.ForeignKey("R_id"))    