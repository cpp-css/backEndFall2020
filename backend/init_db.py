from config import db
from database import session, receipt, notification, contact

db.create_all()
print('success')