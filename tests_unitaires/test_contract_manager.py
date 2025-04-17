import unittest 
from unittest.mock import MagicMock
from datetime import date 
from controls.contract_manager import ContractManager
from models.models import Contract






class TestContractManager(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.manager = ContractManager(self.mock_db)


    def test_create_contract(self):
        contract_data = {
            "client_id": 1,
            "commercial_id": 2,
            "total_amount": 5000.00,
            "remaining_amount": 1500.00,
            "status_contract": True
        }

        result = self.manager.create_contract(**contract_data)

        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()

        self.assertIsInstance(result, Contract)
        self.assertEqual(result.total_amount, 5000.00)
        self.assertTrue(result.status_contract)

    def test_update_contract(self):
        contract = Contract(
            id=1,
            client_id=1,
            commercial_id=2,
            total_amount=5000.00,
            remaining_amount=1500.00,
            created_date=date.today(),
            status_contract=False
        )

        self.mock_db.query().filter().first.return_value = contract

        updated_data = {"status_contract": True, "remaining_amount": 0.0}
        result = self.manager.update_contract(1, updated_data)

        self.assertEqual(result.status_contract, True)
        self.assertEqual(result.remaining_amount, 0.0)
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()

    def test_update_not_found(self):
        self.mock_db.query().filter().first.return_value = None
        
        result = self.manager.update_contract(1, {"status_contract": False})

        self.assertIsNone(result)
        self.mock_db.commit.assert_not_called()


    def test_get_contract(self):
        contract = Contract(id=1, total_amount=3000.00)
        self.mock_db.query().filter().first.return_value = contract

        result = self.manager.get_contract(1)

        self.assertEqual(result.id, 1)
        self.assertEqual(result.total_amount, 3000.00)

    def test_get_unsigned_contract(self):
        contracts = [Contract(status_contract=False)]
        self.mock_db.query().filter().all.return_value = contracts

        result = self.manager.get_unsigned_contract(2)

        self.assertEqual(len(result), 1)
        self.assertFalse(result[0].status_contract)


    def test_get_unpaid_contracts(self):
        contracts = [Contract(remaining_amount=1000.00)]

        self.mock_db.query().filter().all.return_value = contracts

        result = self.manager.get_unpaid_contract(2)

        self.assertEqual(len(result), 1)
        self.assertGreater(result[0].remaining_amount, 0)



if __name__ == '__main__':
    unittest.main()
