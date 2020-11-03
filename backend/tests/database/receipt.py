from datetime import datetime
import unittest
from config import db
from database.registration import Registration
from tests.utils import MAGIC_TEXT

class RegistrationTest(unittest.TestCase):

    def test_receipt(self):
        # generate object and save to db
        receipt = Registration(0, 0, MAGIC_TEXT, MAGIC_TEXT, MAGIC_TEXT)
        db.session.add(receipt)
        db.session.commit()
        
        # attempt to fetch receipt
        receipt = db.session.query(Registration).limit(1).first()
        
        # test explicit data
        #self.assertEqual(receipt.sender_id, 0)
        self.assertEqual(receipt.register_id, 0)
        self.assertEqual(receipt.event_id, 0)
        self.assertEqual(receipt.type, MAGIC_TEXT)
        self.assertEqual(receipt.info, MAGIC_TEXT)
        self.assertEqual(receipt.qr, MAGIC_TEXT)

        # test implicit data
        self.assertLess(receipt.created_at, datetime.utcnow())
        
        # cleanup
        db.session.delete(receipt)
        db.session.commit()
