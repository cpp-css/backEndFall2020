import uuid
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.dialects.postgresql import UUID
from config import db
from database.event import Event
from database.notification import Notification

ph = PasswordHasher()

class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    email = db.Column(db.Unicode(254), unique=True, nullable=False)
    _password = db.Column('password', db.String(255), nullable=False)
    name = db.Column(db.Unicode(120), nullable=False)
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
        