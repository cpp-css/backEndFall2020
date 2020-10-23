from config import db, ma
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Organization(db.Model):
    __tablename__ = 'Organization'
    organization_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    chairman_id = db.Column(UUID(as_uuid=True), db.ForeignKey('User.user_id'), nullable=False)
    admin_id = db.Column(UUID(as_uuid=True), db.ForeignKey('User.user_id'))
    contact_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Contact.contact_id'), nullable=False)
    org_name = db.Column(db.String(250), nullable=False)
    categories = db.Column(db.String(250), nullable=False)

    '''def __init__(self, org_name, categories):
        self.org_name = org_name
        self.categories = categories'''


class OrganizationSchema(ma.Schema):
    class Meta:
        fields = ('organization_id', 'chairman_id', 'admin_id', 'org_name', 'categories')
