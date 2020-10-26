import uuid
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.dialects.postgresql import UUID
from config import db, ma
from database.role import Role

ph = PasswordHasher()


class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    email = db.Column(db.Unicode(254), unique=True, nullable=False)
    _password = db.Column('password', db.String(255), nullable=False)
    name = db.Column(db.Unicode(120), nullable=False)

    registered_events = db.relationship('Event', lazy=True)
    notifications_sent = db.relationship('Notification', lazy='dynamic', foreign_keys='Notification.sender_id')
    notifications_received = db.relationship('Notification', lazy='dynamic', foreign_keys='Notification.receiver_id')
    receipts_sent = db.relationship('Receipt', lazy='dynamic', foreign_keys='Receipt.sender_id')
    receipts_received = db.relationship('Receipt', lazy='dynamic', foreign_keys='Receipt.receiver_id')
    roles = db.relationship('Role', lazy='dynamic')
    sessions = db.relationship('Session', lazy='dynamic')

    @classmethod
    def schema(cls):
        class Schema(SQLAlchemySchema):
            class Meta:
                model = User

            name = auto_field()
            roles = Nested(Role.schema(), many=True)

        if (not hasattr(cls, '_schema')): cls._schema = Schema()
        return cls._schema

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = ph.hash(password)

    def verify_password(self, password):
        try:
            return ph.verify(self._password, password)
        except (VerifyMismatchError):
            return False

    def dump(self):
        return User.schema().dump(self)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('name', 'user_id', 'email', )