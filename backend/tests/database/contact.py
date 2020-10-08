import unittest
from datetime import datetime
from config import db
from database.contact import Contact
from tests.utils import MAGIC_TEXT, STATE


class ContactTest(unittest.TestCase):

    def test_notification(self):
        # generate object and save to db
        current_time = datetime.utcnow()
        contact = Contact(current_time, 0, MAGIC_TEXT, STATE, 0, MAGIC_TEXT)
        db.session.add(contact)
        db.session.commit()

        # attempt to fetch notification
        contact = db.session.query(Contact).limit(1).first()

        # test explicit data
        self.assertEqual(contact.dob, current_time)
        self.assertEqual(contact.phone, 0)
        self.assertEqual(contact.address, MAGIC_TEXT)
        self.assertEqual(contact.state, STATE)
        self.assertEqual(contact.zipcode, 0)
        self.assertEqual(contact.country, MAGIC_TEXT)

        # test implicit data
        self.assertLess(contact.dob, datetime.utcnow())

        # cleanup
        db.session.delete(contact)
        db.session.commit()