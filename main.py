# main.py
from database.db_manager import create_tables
from ui.navigator import Navigator

def main():
    # Initialize database
    create_tables()
    
    # Start application
    navigator = Navigator()
    navigator.start()

if __name__ == "__main__":
    main()