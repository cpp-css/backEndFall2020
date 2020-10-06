import unittest
from config import db
from database.organization import Organization
from tests.utils import MAGIC_TEXT


class OrganizationTest(unittest.TestCase):

    def test_organization(self):
        organization = Organization (0,0,0,MAGIC_TEXT,MAGIC_TEXT)
        db.session.add(organization)
        db.session.commit()

        organization = db.sessions.query(Organization).limit(1).first()

        self.assertEqual(organization.chairman_id, 0)
        self.assertEqual(organization.admin_id, 0)
        self.assertEqual(organization.contact_id, 0)
        self.assertEqual(organization.org_names, MAGIC_TEXT)
        self.assertEqual(organization.categories, MAGIC_TEXT)

        self.assertLess(organization.created_at, datetime.utcnow())

        db.session.delete(organization)
        db.session.commit()
