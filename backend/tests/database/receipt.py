from datetime import datetime
import unittest
from config import db
from database.receipt import Receipt
from tests.utils import MAGIC_TEXT

class ReceiptTest(unittest.TestCase):

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
