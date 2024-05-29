from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
db = SQLAlchemy()


viewers = db.Table(
    "customer_restaurant_association",
    db.Column("customer_id", db.Integer, db.ForeignKey("customer.C_id"), primary_key=True),
    db.Column("restaurant_id", db.Integer, db.ForeignKey("restaurant.R_id"), primary_key=True)                                           
)

orders = db.Table( 
    "order_items",
    db.Column("order_id",db.Integer,db.ForeignKey("order.O_id"),primary_key=True),
    db.Column("item_id",db.Integer,db.ForeignKey("items.I_id"),primary_key=True)
)

class Restaurant(db.Model):
    R_id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), unique=True, nullable = False)
    Email = db.Column(db.String(50), unique=True, nullable= False)
    Address = db.Column(db.String(100), nullable=False)
    Password = db.Column(db.String(128), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    Description = db.Column(db.String(1000), nullable=False)
    Delivery_radius = db.Column(db.String, nullable = False)
    Opening_hours = db.Column(db.String(255), nullable = False)
    customers = db.relationship("Customer",secondary = viewers, backref = db.backref("'viewed_restaurants', lazy=True"))
 #   menu = db.relationship("Menu", backref="Restaurant" ,uselist = False)
    orders = db.relationship("Order",backref="Restaurant",lazy=True)
    def set_pass(self,password):
        self.Password=generate_password_hash(password)
    def check(self,password):
        return check_password_hash(self.Password,password)
    def set_deliveryradius(self, start, end):
        try:
            self.Delivery_radius = json.dumps([str(i) for i in range(int(start), int(end) + 1)])
        except Exception as e:
            print(f"Error in setting delivery radius: {e}")   
    def get_deliverradius(self):
        try:
            return json.loads(self.Delivery_radius)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return []    
        except Exception as e:
            print(f"Error in getting the radius: {e}")
            return []

class Customer(db.Model):
    C_id = db.Column(db.Integer, primary_key = True)
    Email = db.Column(db.String(50), unique=True, nullable = False)
    First_Name = db.Column(db.String(50), nullable = False)
    Last_Name = db.Column(db.String(50), nullable = False)
    Address = db.Column(db.String(100), nullable=False)
    Password = db.Column(db.String, nullable=False)
    Zip = db.Column(db.Integer, nullable = False) 
    restaurants = db.relationship("Restaurant",secondary = viewers, backref = db.backref("'viewers', lazy=True"))
    orders = db.relationship("Order",backref="Customer",lazy=True)
    def set_pass(self,password):
        self.Password=generate_password_hash(password)  
    def check(self,password):
        return check_password_hash(self.Password,password)
#class Menu(db.Model):
 #   M_id = db.Column(db.Integer, primary_key = True)
 #   R_id = db.Column(db.Integer, db.ForeignKey("R_id"))
  #  items = db.relationship("Items",backref="Menu",lazy=True)

class Items(db.Model):
    I_id = db.Column(db.Integer, primary_key = True)
    Category = db.Column(db.String(50), nullable = False)    
    Name = db.Column(db.String(50), nullable = False)
    Price = db.Column(db.Integer, nullable = False)
    Description = db.Column(db.String(1000), nullable = False)
    Picture = db.Column(db.String(255), nullable = True)
    R_id = db.Column(db.Integer,db.ForeignKey("restaurant.R_id"),nullable=False)
    Total_price = db.Column(db.Integer,nullable=True)
   # menu_id = db.Column(db.Integer, db.ForeignKey("M_id"))
    restaurant = db.relationship("Restaurant",backref="Items")
    orders = db.relationship("Order",secondary=orders,backref="Items") 

class Order(db.Model):
    O_id = db.Column(db.Integer, primary_key=True)
    State = db.Column(db.String(50), nullable=False)
    Date = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.C_id"), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.R_id"), nullable=False) 
    items = db.relationship("Items",secondary=orders,backref="Order")
        