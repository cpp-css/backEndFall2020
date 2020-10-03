from datetime import datetime
import unittest
from config import db
from database.notification import Notification
from tests.utils import MAGIC_TEXT

class NotificationTest(unittest.TestCase):

    def test_notification(self):
        # generate object and save to db
        notification = Notification(0, 0, 0, MAGIC_TEXT, MAGIC_TEXT)
        db.session.add(notification)
        db.session.commit()
        
        # attempt to fetch notification
        notification = db.session.query(Notification).limit(1).first()
        
        # test explicit data
        self.assertEqual(notification.sender_id, 0)
        self.assertEqual(notification.receiver_id, 0)
        self.assertEqual(notification.event_id, 0)
        self.assertEqual(notification.type, MAGIC_TEXT)
        self.assertEqual(notification.info, MAGIC_TEXT)

        # test implicit data
        self.assertLess(notification.created_at, datetime.utcnow())
        
        # cleanup
        db.session.delete(notification)
        db.session.commit()
