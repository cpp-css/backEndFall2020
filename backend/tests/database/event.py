from datetime import datetime
import unittest
from config import db
from database.event import Event
from tests.utils import MAGIC_TEXT

class EventTest(unittest.TestCase):

    def test_event(self):
        # generate object and save to db
        current_time = datetime.utcnow()
        event = Event(0, 0, current_time, current_time, MAGIC_TEXT, MAGIC_TEXT, MAGIC_TEXT, MAGIC_TEXT, 0, 0)
        db.session.add(event)
        db.session.commit()

        # attempt to fetch notification
        event = db.session.query(Event).limit(1).first()

        # test explicit data
        self.assertEqual(event.creator_id, 0)
        self.assertEqual(event.organization_id, 0)
        self.assertEqual(event.start_date, current_time)
        self.assertEqual(event.end_date, current_time)
        self.assertEqual(event.theme, MAGIC_TEXT)
        self.assertEqual(event.perks, MAGIC_TEXT)
        self.assertEqual(event.categories, MAGIC_TEXT)
        self.assertEqual(event.info, MAGIC_TEXT)
        self.assertEqual(event.phase, 0)
        self.assertEqual(event.contact_id, 0)

        # test implicit data
        self.assertLess(event.start_date, datetime.utcnow())
        self.assertLess(event.end_date, datetime.utcnow())

        # cleanup
        db.session.delete(event)
        db.session.commit()