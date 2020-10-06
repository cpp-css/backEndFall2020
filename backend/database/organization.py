from config import db

class Organization(db.Model):
    __tablename__ = 'organization'
    organization_id = db.Column(db.Integer, primary_key = True)
    chairman_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False)
    admin_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable = False)
    contact_id = db.Column(db.Integer, db.ForeignKey('Contact.contact_id'), nullable = False)
    org_name = db.Colum(db.String(250), nullable = False)
    categories = db.Column(db.String(250), nullable = False)

    def __init__(self, chairman_id, admin_id, contact_id, org_name, categories):
        self.chairman_id = chairman_id
        self.admin_id = admin_id
        self.contact_id = contact_id
        self.org_name = org_name
        self.categories = categories


