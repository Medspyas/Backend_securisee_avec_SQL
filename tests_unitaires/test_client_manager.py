import unittest 
from unittest.mock import MagicMock
from datetime import date 
from controls.client_manager import ClientManager
from models.models import Client



class TestClientManager(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.manager = ClientManager(self.mock_db)

    def test_create_client(self):
        client_data = {
            "full_name": "joe dalton",
            "email": "joe@mail.com",
            "phone_number":"0600000000",
            "company_name": "Dupont SARL",
            "commercial_id": 1
        }

        result = self.manager.create_client(**client_data)

        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()

        self.assertIsInstance(result, Client)
        self.assertEqual(result.full_name, "joe dalton")
        self.assertEqual(result.email, "joe@mail.com")

    def test_update_client(self):
        client = Client(
            id=1,
            full_name="name",
            email="name@mail.com",
            phone_number="0600000000",
            company_name="name SARL",
            created_date=date.today(),
            updated_date=date.today(),
            commercial_id=1
        )

        self.mock_db.query().filter().first.return_value = client

        updated_data = {"full_name": "names", "company_name": "New SARL"}

        updated_client = self.manager.update_client(1, updated_data)

        self.assertEqual(updated_client.full_name, "names")
        self.assertEqual(updated_client.company_name, "New SARL")
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()

    def test_update_not_found(self):
        self.mock_db.query().filter().first.return_value = None

        result = self.manager.update_client(1, {"full_name": "toto"})

        self.assertIsNone(result)
        self.mock_db.commit.assert_not_called()

    def test_get_client(self):
        client = [
            Client(id=1, full_name="Client 1"),
            Client(id=2, full_name="Client 2")
        ]
        self.mock_db.query().all.return_value = client

        result = self.manager.get_all_client()


        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].full_name, "Client 1")
        

if __name__ == '__main__':
    unittest.main()