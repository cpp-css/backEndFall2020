from datetime import datetime
from config import db


class Event(db.Model):
    __tablename__ = 'Event'
    event_id = db.Column(db.Integer, primary_key=True)
    #creator_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    #organization_id = db.Column(db.Integer, db.ForeignKey('organization.user_id'), nullable=False)
    creator_id = db.Column(db.Integer, nullable=False)  # STUB
    organization_id = db.Column(db.Integer, nullable=False) # STUB
    start_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    theme = db.Column(db.String(250), nullable=False)
    perks = db.Column(db.String(250), nullable=False)
    categories = db.Column(db.String(250), nullable=False)
    info = db.Column(db.String(2500), nullable=False)
    phase = db.Column(db.Integer)
    #contact_id = db.Column(db.Integer, db.ForeignKey('contact.contact_id'), nullable=False)
    contact_id = db.Column(db.Integer, nullable=False) # STUB

    def __init__(self, creator_id, organization_id, start_date, end_date, theme, perks, categories, info, phase, contact_id):
        self.creator_id = creator_id
        self.organization_id = organization_id
        self.start_date = start_date
        self.end_date = end_date
        self.theme = theme
        self.perks = perks
        self.categories = categories
        self.info = info
        self.phase = phase
        self.contact_id = contact_id

