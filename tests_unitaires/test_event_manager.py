import unittest
from datetime import datetime
from unittest.mock import MagicMock

from controls.event_manager import EventManager
from models.models import Client, Contract, Event

"""
    Tests unitaires pour la classe EventManager:
        - création d'événements valides ou refusés selon les conditions,
        - récupération des événements (globaux, par rapport, sans support)
"""


class TestEventManager(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.manager = EventManager(self.mock_db)

    def test_create_event(self):
        self.mock_db.query().filter().first.side_effect = [
            Contract(id=1, client_id=10, status_contract=True),
            Client(id=10, commercial_id=2),
        ]

        event_data = {
            "contract_id": 1,
            "client_id": 10,
            "event_name": "Conférence 1",
            "event_date_start": datetime(2025, 6, 1, 14, 0),
            "event_date_end": datetime(2025, 6, 1, 20, 0),
            "location": "Paris",
            "attendees": 100,
            "notes": "premiere conference",
            "user_id": 2,
        }

        result = self.manager.create_event(**event_data)

        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()
        self.assertIsInstance(result, Event)
        self.assertEqual(result.event_name, "Conférence 1")

    def test_create_event_failed(self):
        self.mock_db.query().filter().first.return_value = Contract(
            status_contract=False
        )

        result = self.manager.create_event(
            contract_id=1,
            client_id=1,
            event_name="Test",
            event_date_start=datetime.now(),
            event_date_end=datetime.now(),
            location="Test",
            attendees=10,
            notes="",
            user_id=2,
        )

        self.assertIsNone(result)
        self.mock_db.add.assert_not_called()

    def test_get_all_event(self):
        events = [Event(id=1), Event(id=2)]
        self.mock_db.query().all.return_value = events

        result = self.manager.get_all_event()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, 1)

    def test_get_events_for_support(self):
        events = [Event(support_id=5)]
        self.mock_db.query.return_value = self.mock_db.query()
        self.mock_db.query().filter().all.return_value = events

        result = self.manager.get_events_for_support(5)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].support_id, 5)

    def test_get_events_without_support(self):
        events = [Event(support_id=None)]
        self.mock_db.query.return_value = self.mock_db.query()
        self.mock_db.query().filter().all.return_value = events

        result = self.manager.get_events_without_support()

        self.assertEqual(len(result), 1)
        self.assertIsNone(result[0].support_id)


if __name__ == "__main__":
    unittest.main()
