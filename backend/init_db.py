from config import db
from database import session, receipt, notification, contact, event, organization, user, role
from datetime import datetime


def create_db():
    db.delete(session.Session)
    db.delete(receipt.Receipt)
    db.delete(notification.Notification)
    db.delete(contact.Contact)
    db.delete(event.Event)
    db.delete(organization.Organization)
    db.delete(user.User)

    db.create_all()

    test_contact = contact.Contact(dob=datetime.utcnow(),
                                   phone=123456,
                                   address="123 South st, City",
                                   state="California",
                                   zipcode=90732,
                                   country="USA")
    test_contact1 = contact.Contact(dob=datetime.utcnow(),
                                    phone=7146523,
                                    address="123 Harbor st, City",
                                    state="California",
                                    zipcode=90882,
                                    country="USA")
    db.session.add(test_contact)
    db.session.add(test_contact1)

    test_user = user.User(password="password",
                          email="test@gmail.com",
                          name="Phuong Nguyen")
    test_user1 = user.User(password="passwordtest",
                           email="khuong@gmail.com",
                           name="Khuong Le")
    db.session.add(test_user)
    db.session.add(test_user1)

    test_org = organization.Organization(org_name="Computer Science Society",
                                         categories="CS",
                                         contact=test_contact)

    test_org1 = organization.Organization(org_name="Software Engineer Association",
                                          categories="CS",
                                          contact=test_contact1)
    db.session.add(test_org)
    db.session.add(test_org1)

    test_role = role.Role(user=test_user,
                          organization=test_org,
                          role=role.Roles.CHAIRMAN)

    test_role1 = role.Role(user=test_user1,
                           organization=test_org1,
                           role=role.Roles.CHAIRMAN)

    db.session.add(test_role)
    db.session.add(test_role1)

    temp_id = db.session.query(user.User).first()
    test_session = session.Session(user_id=temp_id.user_id,
                                   expires=datetime.now())

    db.session.add(test_session)

    db.session.commit()


create_db()
