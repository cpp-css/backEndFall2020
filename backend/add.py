from config import db
from database import session, receipt, notification, contact, event, organization, user, role
from datetime import datetime


def create_new_member():
    test_user = user.User(password="johnbrian",
                          email="john_brian@gmail.com",
                          name="John B")
    test_session = session.Session(user=test_user,
                                   expires=datetime.now())
    db.session.add(test_session)
    db.session.commit()


create_new_member()
