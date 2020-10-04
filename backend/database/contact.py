from config import db


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