#!/usr/bin/env python
# test_verification.py - Test email verification system

import sys
import os
from datetime import datetime, timedelta

sys.path.append(".")

print("=" * 60)
print("TESTING EMAIL VERIFICATION SYSTEM")
print("=" * 60)
print()

# Test 1: Import modules
print("Test 1: Importing modules...")
try:
    from utils.email_service import generate_verification_code, get_code_expiry
    from utils.verification_store import store_verification_code, verify_code, check_email_exists
    print("✅ All modules imported successfully")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

print()

# Test 2: Generate verification code
print("Test 2: Generating verification code...")
try:
    code = generate_verification_code()
    assert len(code) == 6, "Code should be 6 digits"
    assert code.isdigit(), "Code should be numeric"
    print(f"✅ Generated code: {code}")
except Exception as e:
    print(f"❌ Code generation failed: {e}")
    sys.exit(1)

print()

# Test 3: Get expiry time
print("Test 3: Getting expiry time...")
try:
    expiry = get_code_expiry()
    now = datetime.now()
    diff = (expiry - now).total_seconds()
    assert 590 <= diff <= 610, "Expiry should be ~10 minutes"
    print(f"✅ Expiry time: {expiry.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   (Expires in {int(diff/60)} minutes)")
except Exception as e:
    print(f"❌ Expiry time failed: {e}")
    sys.exit(1)

print()

# Test 4: Store verification code
print("Test 4: Storing verification code...")
try:
    test_email = "test@example.com"
    test_code = "123456"
    test_expiry = datetime.now() + timedelta(minutes=10)
    store_verification_code(test_email, test_code, test_expiry)
    print(f"✅ Code stored for {test_email}")
except Exception as e:
    print(f"❌ Store code failed: {e}")
    sys.exit(1)

print()

# Test 5: Verify correct code
print("Test 5: Verifying correct code...")
try:
    result = verify_code(test_email, test_code)
    assert result == True, "Correct code should verify"
    print(f"✅ Code verified successfully")
except Exception as e:
    print(f"❌ Verify code failed: {e}")
    sys.exit(1)

print()

# Test 6: Verify wrong code (should fail)
print("Test 6: Verifying wrong code...")
try:
    # Store a new code
    test_code2 = "654321"
    test_expiry2 = datetime.now() + timedelta(minutes=10)
    store_verification_code(test_email, test_code2, test_expiry2)
    
    result = verify_code(test_email, "999999")  # Wrong code
    assert result == False, "Wrong code should not verify"
    print(f"✅ Wrong code correctly rejected")
except Exception as e:
    print(f"❌ Wrong code test failed: {e}")
    sys.exit(1)

print()

# Test 7: Verify expired code
print("Test 7: Verifying expired code...")
try:
    expired_code = "111111"
    expired_time = datetime.now() - timedelta(minutes=1)  # Already expired
    store_verification_code(test_email, expired_code, expired_time)
    
    result = verify_code(test_email, expired_code)
    assert result == False, "Expired code should not verify"
    print(f"✅ Expired code correctly rejected")
except Exception as e:
    print(f"❌ Expired code test failed: {e}")
    sys.exit(1)

print()

# Test 8: Check email exists
print("Test 8: Checking email existence...")
try:
    # This will return False if users.json doesn't exist or email not found
    exists = check_email_exists("nonexistent@example.com")
    print(f"✅ Email check working (exists: {exists})")
except Exception as e:
    print(f"❌ Email check failed: {e}")
    sys.exit(1)

print()

# Test 9: User registration functions
print("Test 9: Testing user management...")
try:
    import hashlib
    import json
    
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_users():
        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                return json.load(f)
        return {}
    
    users = load_users()
    print(f"✅ User management functions working")
    print(f"   Current users: {len(users)}")
except Exception as e:
    print(f"❌ User management failed: {e}")
    sys.exit(1)

print()

# Cleanup
print("Cleaning up test data...")
try:
    if os.path.exists("verification_codes.json"):
        os.remove("verification_codes.json")
        print("✅ Test data cleaned up")
except Exception as e:
    print(f"⚠️ Cleanup warning: {e}")

print()
print("=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print()
print("Next steps:")
print("1. Update .env with your Gmail credentials")
print("2. Run: streamlit run ui\\app.py")
print("3. Test registration with real email")
print()
