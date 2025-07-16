# utils/auth_2fa.py
import pyotp
import qrcode
from io import BytesIO
from database.db_manager import db_manager

def generate_2fa_secret(user_id):
    """Generate and store a 2FA secret for a user"""
    secret = pyotp.random_base32()
    db_manager.store_2fa_secret(user_id, secret)
    return secret

def generate_2fa_qr(user_id, secret, email):
    """Generate QR code for 2FA setup"""
    provisioning_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=email,
        issuer_name="Bank System"
    )
    img = qrcode.make(provisioning_uri)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def verify_2fa_code(user_id, code):
    """Verify a 2FA code"""
    secret = db_manager.get_2fa_secret(user_id)
    if not secret:
        return False
    totp = pyotp.TOTP(secret)
    return totp.verify(code)