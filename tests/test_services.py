import unittest
from services.account_service import AccountService
from database.db_manager import db_manager

class TestAccountService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize test database
        db_manager.initialize_database()
        # Create test accounts
        cls.account1 = db_manager.create_account("Test User 1", "password123")
        cls.account2 = db_manager.create_account("Test User 2", "password123")
        # Add initial balance
        db_manager.deposit(cls.account1, 1000)
    
    def test_transfer_funds(self):
        # Test successful transfer
        result = AccountService.transfer_funds(self.account1, self.account2, 500, "Test transfer")
        self.assertTrue(result)
        
        # Verify balances
        acc1 = db_manager.get_account_details(self.account1)
        acc2 = db_manager.get_account_details(self.account2)
        self.assertEqual(acc1['balance'], 500)
        self.assertEqual(acc2['balance'], 500)

if __name__ == "__main__":
    unittest.main()