from config import db
from database import session, receipt, notification, contact, event, organization, user


db.create_all()
