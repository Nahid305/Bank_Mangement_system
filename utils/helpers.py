from datetime import datetime

def format_currency(amount: float) -> str:
    """Format amount as currency string"""
    return f"₹{amount:,.2f}"

def format_date(date_str: str) -> str:
    """Format database date to readable format"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime("%d %b %Y %I:%M %p")
    except:
        return date_str

# utils/helpers.py
def validate_input(value, field_type):
    """Basic input validation"""
    if field_type == "account_number":
        # Allow account numbers of any length, as long as they are digits
        return value.isdigit() and len(value) >= 1 and int(value) > 0
    elif field_type == "password":
        return len(value) >= 8
    return True