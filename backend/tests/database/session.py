from datetime import datetime
import unittest
from config import db
from database.session import Session
from tests.utils import MAGIC_TEXT

class SessionTest(unittest.TestCase):

    def test_session(self):
        # generate object and save to db
        current_time = datetime.utcnow()
        session = Session(0, current_time)
        db.session.add(session)
        db.session.commit()
        
        # attempt to fetch
        session = db.session.query(Session).limit(1).first()
        
        # test explicit data
        self.assertEqual(session.user_id, 0)
        self.assertEqual(session.expires, current_time)

        # test implicit data
        self.assertLess(session.created_at, datetime.utcnow())
        self.assertTrue(session.is_expired())
        
        # cleanup
        db.session.delete(session)
        db.session.commit()
