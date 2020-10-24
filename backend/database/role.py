from enum import Enum
import uuid
from sqlalchemy.dialects.postgresql import UUID
from config import db

class Roles(Enum):
    CHAIRMAN = 0
    ADMIN = 1
    MEMBER = 2

class Role(db.Model):
    __tablename__ = 'Role'
    role_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('User.user_id'), nullable=False)
    organization_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Organization.organization_id'), nullable=False)
    role = db.Column(db.Enum(Roles), nullable=False)