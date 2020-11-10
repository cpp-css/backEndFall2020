from datetime import datetime
from config import db, ma
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Event(db.Model):
    __tablename__ = 'Event'
    event_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    creator_id = db.Column(UUID(as_uuid=True), db.ForeignKey('User.user_id'), nullable=False)
    organization_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Organization.organization_id'), nullable=False)
    event_name = db.Column(db.String(250), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    theme = db.Column(db.String(250), nullable=False)
    perks = db.Column(db.String(250), nullable=False)
    categories = db.Column(db.String(250), nullable=False)
    info = db.Column(db.String(2500), nullable=False)
    phase = db.Column(db.Integer, nullable=False)
    contact_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Contact.contact_id'), nullable=False)
    image_url = db.Column(db.String(255))

    creator = db.relationship('User', lazy=True)
    organization = db.relationship('Organization', lazy=True)
    contact = db.relationship('Contact', lazy=True)

    '''def __init__(self, creator_id, organization_id, event_name, start_date, end_date, theme, perks, categories, info, phase, contact_id):
        self.creator_id = creator_id
        self.organization_id = organization_id
        self.event_name = event_name
        self.start_date = start_date
        self.end_date = end_date
        self.theme = theme
        self.perks = perks
        self.categories = categories
        self.info = info
        self.phase = phase
        self.contact_id = contact_id'''


class EventSchema(ma.Schema):
    class Meta:
        fields = ('event_id', 'creator_id', 'organization_id', 'event_name', 'start_date', 'end_date', 'theme', 'perks', 'categories', 'info', 'phase', 'contact_id')