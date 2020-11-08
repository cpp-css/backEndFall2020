from enum import Enum
import uuid
from sqlalchemy.dialects.postgresql import UUID
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from config import db, ma


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

    user = db.relationship('User', lazy=True)
    organization = db.relationship('Organization', lazy=True)

    @classmethod
    def schema(cls):
        class Schema(SQLAlchemySchema):
            class Meta:
                model = Role

            organization_id = auto_field()
            role = EnumField(Roles)

        if (not hasattr(cls, '_schema')): cls._schema = Schema()
        return cls._schema

    def dump(self):
        return Role.schema().dump(self)

class RoleSchema(ma.Schema):
    class Meta:
        fields = 'user_id'
