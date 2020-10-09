from config import db

class User(db.Model):
    __tablename__ = 'Event'
    user_id = db.Column(db.String(120), primary_key = True);
    user_password = db.Column(db.String(120), nullable=False)
    user_email = db.Column(db.String(120), unique = True, nullable=False)
    user_role = db.Column(db.String(120), unique = True, nullable=False)
    user_contact = db.Column(db.String(120), unique = True, nullable=False)

    def __init__(self, user_id, user_password, user_email, user_role, user_contact):
        self.user_id = user_id
        self.user_password = user_password
        self.user_email = user_email
        self.user_role = user_role
        self.user_contact = user_contact
