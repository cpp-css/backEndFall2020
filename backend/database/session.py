from datetime import datetime
from secrets import token_hex
from config import db

class Session(db.Model):
    def __gen_id(): return token_hex(16)
    
    __tablename__ = 'Session'
    session_id = db.Column(db.String(32), primary_key=True, default=__gen_id)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False) # STUB
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, user_id, expires):
        self.user_id = user_id
        self.expires = expires
        
    def is_expired(self):
        return (self.expires < datetime.utcnow())
