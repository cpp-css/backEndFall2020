from config import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Organization(db.Model):
    __tablename__ = 'Organization'
    organization_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    chairman_id = db.Column(UUID(as_uuid=True), db.ForeignKey('User.user_id'), nullable=False)
    admin_id = db.relationship('User', lazy='subquery', backref=db.backref('Organization', lazy=True))
    contact_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Contact.contact_id'), nullable=False)
    org_name = db.Column(db.String(250), nullable=False)
    categories = db.Column(db.String(250), nullable=False)


    def __init__(self, chairman_id, admin_id, contact_id, org_name, categories):
        self.chairman_id = chairman_id
        self.admin_id = admin_id
        self.contact_id = contact_id
        self.org_name = org_name
        self.categories = categories
