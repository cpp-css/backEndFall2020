from datetime import datetime
import unittest
from config import db
from database.notification import Notification
from database.receipt import Receipt
from database.session import Session

MAGIC_TEXT = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'

class DatabaseTest(unittest.TestCase):

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

    def test_receipt(self):
        # generate object and save to db
        receipt = Receipt(0, 0, 0, MAGIC_TEXT, MAGIC_TEXT, MAGIC_TEXT)
        db.session.add(receipt)
        db.session.commit()
        
        # attempt to fetch receipt
        receipt = db.session.query(Receipt).limit(1).first()
        
        # test explicit data
        self.assertEqual(receipt.sender_id, 0)
        self.assertEqual(receipt.receiver_id, 0)
        self.assertEqual(receipt.event_id, 0)
        self.assertEqual(receipt.type, MAGIC_TEXT)
        self.assertEqual(receipt.info, MAGIC_TEXT)
        self.assertEqual(receipt.qr, MAGIC_TEXT)

        # test implicit data
        self.assertLess(receipt.created_at, datetime.utcnow())
        
        # cleanup
        db.session.delete(receipt)
        db.session.commit()
        
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
