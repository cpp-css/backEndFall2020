from config import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database.event import Event
from database.notification import Notification


class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key = True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    #contact_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Contact.contact_id'), nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    registered_events = db.relationship('Event', backref='User', lazy=True)
    sender = db.relationship('Notification', backref='Sender', lazy=True, foreign_keys='Notification.sender_id')
    receiver = db.relationship('Notification', backref='Receiver', lazy=True, foreign_keys='Notification.receiver_id')
    admin = db.relationship('Organization', backref='admin', lazy=True, foreign_keys='Organization.chairman_id')
    sessions = db.relationship('Session', lazy='subquery', backref=db.backref('User', lazy=True))
    chairman = db.relationship('Organization', backref='chairman', lazy=True, foreign_keys='Organization.chairman_id')

    '''def __init__(self, password, email, role, first_name, last_name):
        self.password = password
        self.email = email
        self.role = role
        self.first_name = first_name
        self.last_name = last_name'''
