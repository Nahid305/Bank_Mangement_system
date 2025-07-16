# database/db_manager.py
import sqlite3
from datetime import datetime
import bcrypt
from typing import Optional, List, Tuple, Dict, Union
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """A class to manage all database operations for the banking system."""
    
    def __init__(self):
        self.db_file = 'bank.db'
        
    def create_connection(self) -> sqlite3.Connection:
        """Create and return a database connection with proper settings."""
        try:
            conn = sqlite3.connect(self.db_file, isolation_level=None)
            conn.execute("PRAGMA foreign_keys = ON")
            conn.row_factory = sqlite3.Row  # Enable dictionary-like access to rows
            return conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {str(e)}")
            raise Exception(f"Database connection failed: {str(e)}")
    
    def initialize_database(self) -> None:
        """Initialize the database with required tables and default admin."""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS accounts (
                account_number INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                balance REAL NOT NULL DEFAULT 0.0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT balance_non_negative CHECK (balance >= 0)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number INTEGER NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_number) REFERENCES accounts(account_number) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS admin (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                last_login DATETIME
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS loan_applications (
                application_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number INTEGER NOT NULL,
                income REAL NOT NULL,
                credit_score INTEGER NOT NULL,
                loan_amount REAL NOT NULL,
                loan_term INTEGER NOT NULL,
                status TEXT DEFAULT 'Pending',
                decision_date DATETIME,
                FOREIGN KEY (account_number) REFERENCES accounts(account_number)
            )
            """
        ]
        
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            
            # Create tables
            for table in tables:
                cursor.execute(table)
            
            # Check if admin exists
            cursor.execute("SELECT COUNT(*) FROM admin")
            if cursor.fetchone()[0] == 0:
                # Create default admin (password should be changed after first login)
                hashed_pwd = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
                cursor.execute(
                    "INSERT INTO admin (username, password, full_name) VALUES (?, ?, ?)",
                    ("admin", hashed_pwd, "System Administrator")
                )
            
            conn.commit()
            logger.info("Database initialized successfully")
        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Database initialization failed: {str(e)}")
            raise Exception(f"Database initialization failed: {str(e)}")
        finally:
            conn.close()

    # Account Management
    def create_account(self, name: str, password: str) -> Optional[int]:
        """Create a new bank account with hashed password."""
        if not name or not password:
            logger.warning("Account creation failed: empty name or password")
            return None
            
        if len(password) < 8:
            logger.warning("Account creation failed: password too short")
            return None
            
        hashed_pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO accounts (name, password) VALUES (?, ?)",
                (name.strip(), hashed_pwd)
            )
            account_number = cursor.lastrowid
            conn.commit()
            logger.info(f"Account created successfully: #{account_number}")
            return account_number
        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Account creation failed: {str(e)}")
            return None
        finally:
            conn.close()

    def authenticate_user(self, account_number: str, password: str) -> bool:
        """Authenticate a user with bcrypt password verification."""
        try:
            account_number = int(account_number)
        except ValueError:
            logger.warning(f"Authentication failed: invalid account number format {account_number}")
            return False
            
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT password FROM accounts WHERE account_number = ?",
                (account_number,)
            )
            result = cursor.fetchone()
            
            if result:
                stored_hash = result["password"]
                if isinstance(stored_hash, str):
                    stored_hash = stored_hash.encode()
                return bcrypt.checkpw(password.encode(), stored_hash)
            return False
        except sqlite3.Error as e:
            logger.error(f"Authentication error: {str(e)}")
            return False
        finally:
            conn.close()

    def authenticate_admin(self, username: str, password: str) -> bool:
        """Authenticate an admin user."""
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT password FROM admin WHERE username = ?",
                (username.lower(),)
            )
            result = cursor.fetchone()
            
            if result:
                stored_hash = result["password"]
                if isinstance(stored_hash, str):
                    stored_hash = stored_hash.encode()
                
                if bcrypt.checkpw(password.encode(), stored_hash):
                    # Update last login time
                    cursor.execute(
                        "UPDATE admin SET last_login = CURRENT_TIMESTAMP WHERE username = ?",
                        (username.lower(),)
                    )
                    conn.commit()
                    return True
            return False
        except sqlite3.Error as e:
            logger.error(f"Admin authentication error: {str(e)}")
            return False
        finally:
            conn.close()

    # Transaction Management
    def deposit(self, account_number: int, amount: float, description: str = "Deposit") -> bool:
        """Deposit money into an account."""
        if amount <= 0:
            logger.warning(f"Deposit failed: invalid amount {amount}")
            return False
            
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            
            # Start transaction
            cursor.execute("BEGIN TRANSACTION")
            
            # Update balance
            cursor.execute(
                "UPDATE accounts SET balance = balance + ? WHERE account_number = ?",
                (amount, account_number)
            )
            
            # Record transaction
            cursor.execute(
                "INSERT INTO transactions (account_number, type, amount, description) VALUES (?, ?, ?, ?)",
                (account_number, "Deposit", amount, description)
            )
            
            conn.commit()
            logger.info(f"Deposit successful: ₹{amount} to account #{account_number}")
            return True
        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Deposit failed: {str(e)}")
            return False
        finally:
            conn.close()

    def withdraw(self, account_number: int, amount: float, description: str = "Withdrawal") -> bool:
        """Withdraw money from an account if sufficient balance exists."""
        if amount <= 0:
            logger.warning(f"Withdrawal failed: invalid amount {amount}")
            return False
            
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            
            # Start transaction
            cursor.execute("BEGIN TRANSACTION")
            
            # Check balance
            cursor.execute(
                "SELECT balance FROM accounts WHERE account_number = ?",
                (account_number,)
            )
            balance = cursor.fetchone()["balance"]
            
            if balance < amount:
                logger.warning(f"Withdrawal failed: insufficient balance in account #{account_number}")
                return False
                
            # Update balance
            cursor.execute(
                "UPDATE accounts SET balance = balance - ? WHERE account_number = ?",
                (amount, account_number)
            )
            
            # Record transaction
            cursor.execute(
                "INSERT INTO transactions (account_number, type, amount, description) VALUES (?, ?, ?, ?)",
                (account_number, "Withdrawal", amount, description)
            )
            
            conn.commit()
            logger.info(f"Withdrawal successful: ₹{amount} from account #{account_number}")
            return True
        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Withdrawal failed: {str(e)}")
            return False
        finally:
            conn.close()

    def transfer(self, from_account: int, to_account: int, amount: float, description: str = "Transfer") -> bool:
        """Transfer money between accounts."""
        if amount <= 0:
            logger.warning(f"Transfer failed: invalid amount {amount}")
            return False
            
        if from_account == to_account:
            logger.warning("Transfer failed: cannot transfer to same account")
            return False
            
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            
            # Start transaction
            cursor.execute("BEGIN TRANSACTION")
            
            # Check if recipient exists
            cursor.execute("SELECT 1 FROM accounts WHERE account_number = ?", (to_account,))
            if not cursor.fetchone():
                logger.warning(f"Transfer failed: recipient account #{to_account} not found")
                return False
                
            # Check sender balance
            cursor.execute(
                "SELECT balance FROM accounts WHERE account_number = ?",
                (from_account,)
            )
            balance = cursor.fetchone()["balance"]
            
            if balance < amount:
                logger.warning(f"Transfer failed: insufficient balance in account #{from_account}")
                return False
                
            # Perform transfer
            # Deduct from sender
            cursor.execute(
                "UPDATE accounts SET balance = balance - ? WHERE account_number = ?",
                (amount, from_account)
            )
            cursor.execute(
                "INSERT INTO transactions (account_number, type, amount, description) VALUES (?, ?, ?, ?)",
                (from_account, "Transfer Out", amount, f"To #{to_account}: {description}")
            )
            
            # Add to recipient
            cursor.execute(
                "UPDATE accounts SET balance = balance + ? WHERE account_number = ?",
                (amount, to_account)
            )
            cursor.execute(
                "INSERT INTO transactions (account_number, type, amount, description) VALUES (?, ?, ?, ?)",
                (to_account, "Transfer In", amount, f"From #{from_account}: {description}")
            )
            
            conn.commit()
            logger.info(f"Transfer successful: ₹{amount} from #{from_account} to #{to_account}")
            return True
        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Transfer failed: {str(e)}")
            return False
        finally:
            conn.close()

    # Account Information
    def get_balance(self, account_number: int) -> Optional[float]:
        """Get current balance of an account."""
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT balance FROM accounts WHERE account_number = ?",
                (account_number,)
            )
            result = cursor.fetchone()
            return result["balance"] if result else None
        except sqlite3.Error as e:
            logger.error(f"Balance check failed: {str(e)}")
            return None
        finally:
            conn.close()

    def get_account_details(self, account_number: int) -> Optional[Dict]:
        """Get all details of an account."""
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT account_number, name, balance, created_at FROM accounts WHERE account_number = ?",
                (account_number,)
            )
            result = cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error as e:
            logger.error(f"Account details fetch failed: {str(e)}")
            return None
        finally:
            conn.close()

    def get_transactions(self, account_number: int, limit: int = 100) -> List[Dict]:
        """Get transaction history for an account."""
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT type, amount, description, timestamp 
                FROM transactions 
                WHERE account_number = ?
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (account_number, limit)
            )
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Transaction history fetch failed: {str(e)}")
            return []
        finally:
            conn.close()

    # Admin Functions
    def get_all_accounts(self) -> List[Dict]:
        """Get all accounts in the system (admin only)."""
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT account_number, name, balance, created_at FROM accounts ORDER BY account_number"
            )
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Account list fetch failed: {str(e)}")
            return []
        finally:
            conn.close()

    def delete_account(self, account_number: int) -> bool:
        """Delete an account and all its transactions (admin only)."""
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            
            # Verify account exists
            cursor.execute("SELECT 1 FROM accounts WHERE account_number = ?", (account_number,))
            if not cursor.fetchone():
                logger.warning(f"Account deletion failed: account #{account_number} not found")
                return False
                
            # Delete account (transactions will be deleted automatically due to ON DELETE CASCADE)
            cursor.execute("DELETE FROM accounts WHERE account_number = ?", (account_number,))
            conn.commit()
            logger.info(f"Account deleted successfully: #{account_number}")
            return True
        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Account deletion failed: {str(e)}")
            return False
        finally:
            conn.close()

    # Loan Management
    def submit_loan_application(self, account_number: int, income: float, credit_score: int, 
                              loan_amount: float, loan_term: int, status: str = "Pending") -> bool:
        """Submit a loan application with optional predicted status."""
        if income <= 0 or loan_amount <= 0 or loan_term <= 0:
            return False
            
        if credit_score < 300 or credit_score > 850:
            return False
            
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO loan_applications 
                (account_number, income, credit_score, loan_amount, loan_term, status, decision_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (account_number, income, credit_score, loan_amount, loan_term, status, 
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S") if status != "Pending" else None)
            )
            conn.commit()
            return True
        except sqlite3.Error:
            conn.rollback()
            return False
        finally:
            conn.close()

    def get_loan_applications(self, account_number: Optional[int] = None) -> List[Dict]:
        """Get loan applications, optionally filtered by account."""
        conn = self.create_connection()
        try:
            cursor = conn.cursor()
            
            if account_number:
                cursor.execute(
                    """
                    SELECT * FROM loan_applications 
                    WHERE account_number = ?
                    ORDER BY application_id DESC
                    """,
                    (account_number,)
                )
            else:
                cursor.execute(
                    "SELECT * FROM loan_applications ORDER BY application_id DESC"
                )
                
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error:
            return []
        finally:
            conn.close()

# Singleton instance for the application to use
db_manager = DatabaseManager()

# Initialize database when module is imported
db_manager.initialize_database()

# Legacy functions for backward compatibility (can be deprecated later)
def create_tables():
    """Legacy function for initializing database."""
    db_manager.initialize_database()

def create_account(name: str, password: str) -> Optional[int]:
    """Legacy function for account creation."""
    return db_manager.create_account(name, password)

def authenticate(account_number: str, password: str) -> bool:
    """Legacy function for user authentication."""
    return db_manager.authenticate_user(account_number, password)

def admin_authenticate(username: str, password: str) -> bool:
    """Legacy function for admin authentication."""
    return db_manager.authenticate_admin(username, password)

def deposit(account_number: int, amount: float) -> bool:
    """Legacy function for deposits."""
    return db_manager.deposit(account_number, amount)

def withdraw(account_number: int, amount: float) -> bool:
    """Legacy function for withdrawals."""
    return db_manager.withdraw(account_number, amount)

def get_balance(account_number: int) -> Optional[float]:
    """Legacy function for balance check."""
    return db_manager.get_balance(account_number)

def get_transactions(account_number: int) -> List[Tuple]:
    """Legacy function for transaction history."""
    transactions = db_manager.get_transactions(account_number)
    return [(t['type'], t['amount'], t['timestamp']) for t in transactions]

def get_all_users() -> List[Tuple]:
    """Legacy function for getting all users."""
    accounts = db_manager.get_all_accounts()
    return [(a['account_number'], a['name'], a['balance']) for a in accounts]

def delete_user(account_number: int) -> bool:
    """Legacy function for account deletion."""
    return db_manager.delete_account(account_number)