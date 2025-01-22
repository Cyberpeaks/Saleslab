from saleslab import db

#from flask_sqlalchemy import SQLAlchemy
#db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)

# Create Company table
class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(30), nullable=False)
    businessType = db.Column(db.String(30), nullable=False)
    contactPerson = db.Column(db.String(30), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(30), nullable=True)
    status = db.Column(db.String(30), nullable=True, default="CURRENT")
    #flight_id = db.Column(db.Integer, db.ForeignKey("flights.id"), nullable=False)

# Create Customer table
class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)
    location = db.relationship('Location', backref=db.backref('customers', lazy=True))
    phone = db.Column(db.String(30), nullable=True)
    #email = db.Column(db.String(30), nullable=True)
    gender = db.Column(db.String(30), nullable=True)
    doe = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(30), nullable=True, default="CURRENT")

# Create Employee table
class Employee(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    gender = db.Column(db.String(30), nullable=True)
    doe = db.Column(db.Date, nullable=True)
    role = db.Column(db.String(30), nullable=True)
    status = db.Column(db.String(30), nullable=True, default="CURRENT")
    salesPermit = db.Column(db.String(30), nullable=True, default="NO")
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    

# Create Location table
class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    City = db.Column(db.String(30), nullable=False)
    locality = db.Column(db.String(30), nullable=False)

# Create Product table
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(30), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    company = db.relationship('Company', backref=db.backref('products', lazy=True))
    unitPrice = db.Column(db.Float, nullable=False)
    
# Create Sales table
class Sales(db.Model):
    __tablename__ = "sales"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    salesPerson_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    product = db.relationship('Product', backref=db.backref('sales', lazy=True))
    customer = db.relationship('Customer', backref=db.backref('sales', lazy=True))
    employee = db.relationship('Employee', backref=db.backref('sales', lazy=True))
    salesDate = db.Column(db.String(30), nullable=False)
    unitPrice = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    remarks = db.Column(db.String(30), nullable=True)
    
    