from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    username = db.Column(db.Integer, nullable=False)
    password = db.Column(db.Integer, nullable=False)


class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String, nullable=False)
    businesstype = db.Column(db.String, nullable=False)
    contact_person = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=True, default="CURRENT")
    #flight_id = db.Column(db.Integer, db.ForeignKey("flights.id"), nullable=False)

class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)
    phone = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    gender = db.Column(db.String, nullable=True)
    doe = db.Column(db.Date, nullable=True)
    status = db.Column(db.String, nullable=True, default="CURRENT")
    #flight_id = db.Column(db.Integer, db.ForeignKey("flights.id"), nullable=False)
