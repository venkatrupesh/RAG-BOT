# utils/verification_store.py

import json
import os
from datetime import datetime

VERIFICATION_FILE = "verification_codes.json"

def load_codes():
    """Load verification codes from file"""
    if os.path.exists(VERIFICATION_FILE):
        with open(VERIFICATION_FILE, "r") as f:
            return json.load(f)
    return {}

def save_codes(codes):
    """Save verification codes to file"""
    with open(VERIFICATION_FILE, "w") as f:
        json.dump(codes, f, indent=2)

def store_verification_code(email, code, expiry):
    """Store verification code for an email"""
    codes = load_codes()
    codes[email] = {
        "code": code,
        "expiry": expiry.strftime("%Y-%m-%d %H:%M:%S"),
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_codes(codes)

def verify_code(email, code):
    """Verify if the code is correct and not expired"""
    codes = load_codes()
    
    if email not in codes:
        return False
    
    stored = codes[email]
    expiry = datetime.strptime(stored["expiry"], "%Y-%m-%d %H:%M:%S")
    
    # Check if expired
    if datetime.now() > expiry:
        # Clean up expired code
        del codes[email]
        save_codes(codes)
        return False
    
    # Check if code matches
    if stored["code"] == code:
        # Clean up used code
        del codes[email]
        save_codes(codes)
        return True
    
    return False

def check_email_exists(email, users_file="users.json"):
    """Check if email is already registered"""
    if not os.path.exists(users_file):
        return False
    
    with open(users_file, "r") as f:
        users = json.load(f)
    
    for user_data in users.values():
        if user_data.get("email") == email:
            return True
    
    return False
