import unittest
from unittest.mock import MagicMock

from controls.gestion_manager import GestionManager
from models.models import Event, User

"""
    Tests unitaires pour la classe GestionManager:
    - création, mise à jour et à la suppression d'utilisateurs,
    - assignation des supports aux événements.

"""


class TestGestionManager(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.manager = GestionManager(self.mock_db)

    def test_assign_support_to_event(self):
        event = Event(id=1, support_id=None)
        self.mock_db.query().filter().first.return_value = event

        result = self.manager.assign_support_to_event(event_id=1, support_id=5)

        self.assertEqual(result.support_id, 5)
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()

    def test_assign_to_event_not_found(self):
        self.mock_db.query().filter().first.return_value = None

        result = self.manager.assign_support_to_event(1, 5)

        self.assertIsNone(result)
        self.mock_db.commit.assert_not_called()

    def test_create_user(self):
        self.mock_db.query().filter().first.return_value = None

        result = self.manager.create_user(
            first_name="dan",
            last_name="cho",
            email="mail@mail.com",
            password="1234",
            role="support",
        )

        self.assertIsInstance(result, User)
        self.assertEqual(result.first_name, "dan")
        self.assertEqual(result.role.value, "support")
        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()

    def test_create_user_already_exist(self):
        self.mock_db.query().filter().first.return_value = User(email="mail@mail.com")

        result = self.manager.create_user(
            first_name="dan",
            last_name="cho",
            email="mail@mail.com",
            password="1234",
            role="support",
        )

        self.assertIsNone(result)
        self.mock_db.add.assert_not_called()

    def test_update_user(self):
        user = User(id=1, first_name="Hight")
        self.mock_db.query().filter().first.return_value = user

        result = self.manager.updated_user(1, {"first_name": "low"})

        self.assertEqual(result.first_name, "low")
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()

    def test_update_user_not_found(self):
        self.mock_db.query().filter().first.return_value = None

        result = self.manager.updated_user(1, {"first_name": "nobody"})

        self.assertIsNone(result)
        self.mock_db.commit.assert_not_called()

    def test_delete_user(self):
        user = User(id=1)

        self.mock_db.query().filter().first.return_value = user

        result = self.manager.delete_user(1)

        self.assertTrue(result)
        self.mock_db.delete.assert_called_once_with(user)
        self.mock_db.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
