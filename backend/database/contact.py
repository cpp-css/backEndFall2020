from config import db, ma
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
    state = db.Column(db.String(250))
    zipcode = db.Column(db.Integer)
    country = db.Column(db.String(250))
    organization_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Organization.organization_id'))

    organization = db.relationship('Organization', lazy=True, foreign_keys=organization_id)

    '''def __init__(self, dob, phone, address, state, zipcode, country):
        self.dob = dob
        self.phone = phone
        self.address = address
        self.state = state
        self.zipcode = zipcode
        self.country = country'''


class ContactSchema(ma.Schema):
    class Meta:
        fields = ('contact_id', 'dob', 'phone', 'address', 'state', 'zipcode', 'country', 'organization_id')
