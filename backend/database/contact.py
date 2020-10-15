from config import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


# just for storing organization contact information
# if people want then have it for people

class Contact(db.Model):
    __tablename__ = 'Contact'
    contact_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, nullable=False)
    dob = db.Column(db.DateTime)
    phone = db.Column(db.Integer)
    address = db.Column(db.String(250))
    state = db.Column(db.String(10))
    zipcode = db.Column(db.Integer)
    country = db.Column(db.String(250), nullable=False)
    event_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Event.event_id'))
    #organization_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Organization.organization_id'))
    organization = db.relationship('Organization', backref='contact', uselist=False)
    user = db.relationship('User', backref='contact', uselist=False)

    def __init__(self, dob, phone, address, state, zipcode, country):
        self.dob = dob
        self.phone = phone
        self.address = address
        self.state = state
        self.zipcode = zipcode
        self.country = country
