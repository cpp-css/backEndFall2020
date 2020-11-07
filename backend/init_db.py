from config import db
from database import session, registration, notification, contact, event, organization, user, role
from datetime import datetime
import sys
from sqlalchemy.schema import MetaData
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.schema import DropConstraint, DropTable, MetaData, Table

meta = MetaData()


def reset_db():
    # https://github.com/pallets/flask-sqlalchemy/issues/722 reference from bryan5989 
    con = db.engine.connect()
    trans = con.begin()
    inspector = Inspector.from_engine(db.engine)

    '''
    We need to re-create a minimal metadata with only the required things to
    successfully emit drop constraints and tables commands for postgres (based
    on the actual schema of the running instance)
    '''
    meta = MetaData()
    tables = []
    all_fkeys = []

    for table_name in inspector.get_table_names():
        fkeys = []
        for fkey in inspector.get_foreign_keys(table_name):
            if not fkey["name"]:
                continue
            fkeys.append(db.ForeignKeyConstraint((), (), name=fkey["name"]))
        tables.append(Table(table_name, meta, *fkeys))
        all_fkeys.extend(fkeys)

    # drop all the constraint in the data before dropping the table
    for fkey in all_fkeys:
        con.execute(DropConstraint(fkey))

    for table in tables:
        con.execute(DropTable(table))

    trans.commit()


def create_db():
    db.delete(session.Session)
    db.delete(registration.Registration)
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
                          email="phuong@cpp.edu",
                          name="Phuong Nguyen")

    test_user1 = user.User(password="passwordtest",
                           email="khuong@cpp.edu",
                           name="Khuong Le")

    test_user2 = user.User(password="passwordtest",
                           email="josh@cpp.edu",
                           name="Josh")

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

    test_role2 = role.Role(user=test_user2,
                           organization=test_org,
                           role=role.Roles.ADMIN)

    db.session.add(test_role)
    db.session.add(test_role1)
    db.session.add(test_role2)

    temp_id = db.session.query(user.User).first()
    test_session = session.Session(user_id=temp_id.user_id,
                                   expires=datetime.now())

    db.session.add(test_session)

    test_event = event.Event(creator=test_user,
                             organization=test_org,
                             event_name='ADMIN testing',
                             start_date=datetime.now(tz=None),
                             end_date=datetime.now(tz=None),
                             theme='Training',
                             perks='Perks',
                             categories="info",
                             info='categories',
                             phase=0,
                             contact=test_contact)

    test_event1 = event.Event(creator=test_user1,
                              organization=test_org1,
                              event_name='CHAIRMAN testing',
                              start_date=datetime.now(tz=None),
                              end_date=datetime.now(tz=None),
                              theme='Training',
                              perks='Perks',
                              categories="info",
                              info='categories',
                              phase=1,
                              contact=test_contact1)

    test_event2 = event.Event(creator=test_user1,
                              organization=test_org1,
                              event_name='CHAIRMAN testing gg',
                              start_date=datetime.now(tz=None),
                              end_date=datetime.now(tz=None),
                              theme='Training',
                              perks='Perks',
                              categories="info",
                              info='categories',
                              phase=2,
                              contact=test_contact1)
    db.session.add(test_event)
    db.session.add(test_event1)
    db.session.add(test_event2)


    db.session.commit()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Please add 1 argument")
        sys.exit()

    if sys.argv[1] == "reset":
        reset_db()
    elif sys.argv[1] == "create":
        create_db()
    else:
        print("Invalid argument, either reset or create")
        sys.exit()
