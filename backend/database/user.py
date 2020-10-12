from config import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key = True)
    email = db.Column(db.String(120), unique = True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    contact_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Contact.contact_id'), nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    registered_events = db.relationship('Event', backref='User', lazy=True)
    notifications = db.relationship('Notification', backref='User', lazy=True, foreign_keys=['User.sender_id', 'User.receiver_id'])
    admins = db.relationship('Organization', lazy='subquery', backref=db.backref('User', lazy=True))
    sessions = db.relationship('Session', lazy='subquery', backref=db.backref('User', lazy=True))

    def __init__(self, user_id, user_password, user_email, user_role, first_name, last_name, user_contact):
        self.user_id = user_id
        self.password = user_password
        self.email = user_email
        self.role = user_role
        self.contact_id = user_contact
        self.first_name = first_name
        self.last_name = last_name