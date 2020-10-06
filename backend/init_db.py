from config import db
from database import session, receipt, notification, contact, event

db.create_all()
print('success')