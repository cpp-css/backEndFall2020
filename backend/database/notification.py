from datetime import datetime
from config import db

class Notification(db.Model):
    __tablename__ = 'notification'
    notification_id = db.Column(db.Integer, primary_key=True)
    #sender_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    #receiver_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    #event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    sender_id = db.Column(db.Integer, nullable=False) # STUB
    receiver_id = db.Column(db.Integer, nullable=False) # STUB
    event_id = db.Column(db.Integer, nullable=False) # STUB
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    type = db.Column(db.Unicode(250))
    info = db.Column(db.Unicode(2500))

    def __init__(self, sender_id, receiver_id, event_id, type, info, qr):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.event_id = event_id
        self.type = type
        self.info = info
