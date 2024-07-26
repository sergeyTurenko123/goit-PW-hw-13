import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactBase, ContactStatusUpdate, UserModel, UserDb, UserResponse
from src.repository.users import (
    get_contacts,
    get_contact,
    get_contact_name,
    create_contact,
    remove_contact,
    update_contact,
    update_status_contact
)

class TestContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        contact = Contact()
        self.session.query().filter().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contact_name(self):
        contacts = [Contact()]
        self.session.query().filter().first.return_value = contacts
        result = await get_contact_name(name=str, surname=str, email_address=str, phone_number=str, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        body = ContactBase(name="string", surname="string", email_address="string", phone_number="string", date_of_birth="2024-07-25", additional_data="string")
        contact = [Contact(id=1, user_id=1)]
        self.session.query().filter().filter().all.return_value = contact
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email_address, body.email_address)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.date_of_birth, body.date_of_birth)
        self.assertEqual(result.additional_data, body.additional_data)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact(self):
        contact = Contact()
        self.session.query().filter().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_note_not_found(self):
        self.session.query().filter().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact(self):
        body = ContactBase(name="string_name", surname="string", email_address="string", phone_number="string", date_of_birth="2024-07-25", additional_data="string")
        contact = Contact()
        self.session.query().filter().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactBase(name="string_name", surname="string", email_address="string", phone_number="string", date_of_birth="2024-07-25", additional_data="string")
        self.session.query().filter().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_status_contact_found(self):
        body = ContactStatusUpdate(done=True)
        contact = Contact()
        self.session.query().filter().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_status_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_status_note_not_found(self):
        body = ContactStatusUpdate(done=True)
        self.session.query().filter().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_status_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()

