from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

DB_PASSWORD = os.environ.get('DB_PASSWORD')
print(DB_PASSWORD)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:{pw}@localhost:5432/clubs_api'.format(pw=DB_PASSWORD)
app.config['SQLALCHEMY_ECHO'] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Contact(db.Model):
    __tablename__ = 'Contact'
    contact_id = db.Column(db.Integer, primary_key=True, nullable=False)
    dob = db.Column(db.DateTime)
    phone = db.Column(db.Integer)
    address = db.Column(db.String(250))
    state = db.Column(db.String(10))
    zipcode = db.Column(db.Integer)
    country = db.Column(db.String(250), nullable=False)

    def __init__(self, dob, phone, address, state, zipcode, country):
        self.dob = dob
        self.phone = phone
        self.address = address
        self.state = state
        self.zipcode = zipcode
        self.country = country


db.create_all()
