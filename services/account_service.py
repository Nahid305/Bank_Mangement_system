from database.db_manager import db_manager
from utils.helpers import format_currency, format_date

class AccountService:
    @staticmethod
    def get_account_details(account_number: int) -> dict:
        """Get formatted account details"""
        account = db_manager.get_account_details(account_number)
        if account:
            account['formatted_balance'] = format_currency(account['balance'])
            account['formatted_date'] = format_date(account['created_at'])
        return account
    
    @staticmethod
    def transfer_funds(from_acc: int, to_acc: int, amount: float, description: str) -> bool:
        """Handle money transfer with validation"""
        if from_acc == to_acc:
            raise ValueError("Cannot transfer to same account")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return db_manager.transfer(from_acc, to_acc, amount, description)