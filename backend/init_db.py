from config import db
from database import session, receipt, notification, contact, event, organization, user, role


db.create_all()
