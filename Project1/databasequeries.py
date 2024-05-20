from database import Restaurant, Customer, Items, Order, db


def create_user(email, firstname, lastname, address, password, zip):
    customer = Customer(Email = email, First_name = firstname, Last_name = lastname, 
                        Address = address, Password = password,Zip=zip)
    db.session.add(customer)
    db.session.commit()
    return customer

def get_user(email):
    return Customer.query.filter_by(Email = email).first() 

def create_restaurant(name,email,address,password,image,description,deliveryradius,openinghrs):
    restaurant = Restaurant(Name=name,Email=email,Address=address,Password=password,image=image,Description=description,Delivery_radius=deliveryradius,Opening_hours=openinghrs)
    db.session.add(restaurant)
    db.session.commit()
    return restaurant

def get_restaurant(email):
    return Restaurant.query.filter_by(Email=email).first()

def create_menu_item(Category,Name,Price,Description,Picture,Total_price,R_id):
    item = Items(Category=Category,Name=Name,Price=Price,Description=Description,
                 Picture=Picture,Total_price=Total_price,R_id=R_id)
    db.session.add(item)
    db.session.commit()
    return item

def create_order(State,Date,customer_id):
    order = Order(State=State,Date=Date,customer_id=customer_id)
    db.session.add(order)
    db.session.commit()
    return order

def get_orders_of_customer(customer_id):
    return Order.query.filter_by(customer_id=customer_id).all()

def get_items(R_id):
    return Items.query.filter_by(R_id=R_id).all()

