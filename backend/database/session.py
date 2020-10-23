from datetime import datetime
from secrets import token_hex
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from sqlalchemy.dialects.postgresql import UUID
from config import db

class Session(db.Model):
    def __gen_id(): return token_hex(16)
    
    __tablename__ = 'Session'
    session_id = db.Column(db.String(32), primary_key=True, default=__gen_id)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('User.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    
    user = db.relationship('User', backref='Session', lazy=True)
    
    @classmethod
    def schema(cls):
        class Schema(SQLAlchemySchema):
            class Meta:
                model = Session
                
            token = auto_field('session_id')
            expires = auto_field()
        
        if (not hasattr(cls, '_schema')): cls._schema = Schema()
        return cls._schema

    def is_expired(self):
        return (self.expires < datetime.utcnow())

    def dump(self):
        return Session.schema().dump(self)
