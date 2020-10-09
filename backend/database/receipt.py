from datetime import datetime
from config import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Receipt(db.Model):
    __tablename__ = 'Receipt'
    receipt_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    sender_id = db.Column(UUID(as_uuid=True), db.ForeignKey('User.user_id'), nullable=False)
    receiver_id = db.Column(UUID(as_uuid=True), db.ForeignKey('User.user_id'), nullable=False)
    event_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Event.event_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    type = db.Column(db.Unicode(250))
    info = db.Column(db.Unicode(2500))
    qr = db.Column(db.Unicode(250))

    def __init__(self, sender_id, receiver_id, event_id, type, info, qr):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.event_id = event_id
        self.type = type
        self.info = info
        self.qr = qr
