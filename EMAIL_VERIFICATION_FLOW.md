# Email Verification Flow

## Visual Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER REGISTRATION                         │
└─────────────────────────────────────────────────────────────┘

Step 1: User fills registration form
┌──────────────────────────────┐
│  Username: rushikesh         │
│  Email: rushi@gmail.com      │
│  Password: ••••••            │
│                              │
│  [📧 Send Verification Code] │
└──────────────────────────────┘
              ↓
              
Step 2: System validates input
┌──────────────────────────────┐
│  ✓ Password length >= 6      │
│  ✓ Username not taken        │
│  ✓ Email not registered      │
└──────────────────────────────┘
              ↓
              
Step 3: Generate & send code
┌──────────────────────────────┐
│  Generate: 6-digit code      │
│  Example: 847392             │
│  Expiry: 10 minutes          │
│  Send via Gmail SMTP         │
└──────────────────────────────┘
              ↓
              
Step 4: User receives email
┌──────────────────────────────┐
│  📧 Email Inbox              │
│  ─────────────────────────   │
│  From: InterviewAI           │
│  Subject: Verification Code  │
│                              │
│  Your code: 847392           │
│  Expires in 10 minutes       │
└──────────────────────────────┘
              ↓
              
Step 5: User enters code
┌──────────────────────────────┐
│  🔐 Enter 6-digit code       │
│  [8][4][7][3][9][2]          │
│                              │
│  [✅ Verify]  [🔙 Back]      │
└──────────────────────────────┘
              ↓
              
Step 6: System verifies code
┌──────────────────────────────┐
│  ✓ Code matches              │
│  ✓ Not expired               │
│  ✓ Create account            │
│  ✓ Delete used code          │
└──────────────────────────────┘
              ↓
              
Step 7: Success!
┌──────────────────────────────┐
│  🎉 Account Created!         │
│  You can now sign in         │
└──────────────────────────────┘
```

## Technical Flow

```
┌─────────┐      ┌──────────┐      ┌───────────┐      ┌──────────┐
│  User   │      │   App    │      │   Email   │      │  Storage │
│ Browser │      │  Server  │      │  Service  │      │   JSON   │
└────┬────┘      └────┬─────┘      └─────┬─────┘      └────┬─────┘
     │                │                   │                  │
     │ 1. Submit Form │                   │                  │
     │───────────────>│                   │                  │
     │                │                   │                  │
     │                │ 2. Validate       │                  │
     │                │────────────────┐  │                  │
     │                │                │  │                  │
     │                │<───────────────┘  │                  │
     │                │                   │                  │
     │                │ 3. Generate Code  │                  │
     │                │────────────────┐  │                  │
     │                │   (847392)     │  │                  │
     │                │<───────────────┘  │                  │
     │                │                   │                  │
     │                │ 4. Store Code     │                  │
     │                │───────────────────────────────────>  │
     │                │                   │                  │
     │                │ 5. Send Email     │                  │
     │                │──────────────────>│                  │
     │                │                   │                  │
     │                │                   │ 6. Deliver       │
     │<───────────────────────────────────│                  │
     │   (Email)      │                   │                  │
     │                │                   │                  │
     │ 7. Enter Code  │                   │                  │
     │───────────────>│                   │                  │
     │                │                   │                  │
     │                │ 8. Verify Code    │                  │
     │                │<──────────────────────────────────── │
     │                │                   │                  │
     │                │ 9. Create Account │                  │
     │                │────────────────┐  │                  │
     │                │                │  │                  │
     │                │<───────────────┘  │                  │
     │                │                   │                  │
     │ 10. Success ✅ │                   │                  │
     │<───────────────│                   │                  │
     │                │                   │                  │
```

## File Structure

```
RAG-CHATBOT/
├── .env                          ← Email credentials
├── ui/
│   └── app.py                    ← Main app with verification UI
├── utils/
│   ├── email_service.py          ← Send emails via Gmail
│   └── verification_store.py     ← Store & verify codes
├── users.json                    ← User accounts (auto-created)
├── verification_codes.json       ← Temporary codes (auto-created)
└── EMAIL_SETUP_GUIDE.md          ← Setup instructions
```

## Data Storage

### verification_codes.json
```json
{
  "rushi@gmail.com": {
    "code": "847392",
    "expiry": "2026-05-28 14:35:00",
    "created": "2026-05-28 14:25:00"
  }
}
```

### users.json
```json
{
  "rushikesh": {
    "password": "hashed_password_here",
    "email": "rushi@gmail.com",
    "created": "2026-05-28 14:30",
    "interviews": 0
  }
}
```

## Security Features

| Feature | Description |
|---------|-------------|
| **6-digit code** | Random, hard to guess |
| **10-min expiry** | Prevents old code reuse |
| **One-time use** | Code deleted after verification |
| **Email validation** | Ensures real email address |
| **Duplicate check** | Prevents multiple accounts |
| **Password hashing** | SHA-256 encryption |
| **App password** | Not regular Gmail password |

## Error Handling

```
User Input → Validation → Error Messages
    ↓
Username exists? → "Username already exists"
Email exists?    → "Email already registered"
Password short?  → "Password must be 6+ characters"
Email config?    → "Email configuration missing"
Code wrong?      → "Invalid or expired code"
Code expired?    → "Code expired, request new one"
```

## Benefits

✅ **Security**: Prevents fake accounts
✅ **Trust**: Verifies real users
✅ **Professional**: Industry-standard practice
✅ **Spam Prevention**: Reduces abuse
✅ **User Confidence**: Legitimate platform

## Next Steps

1. Follow `QUICK_START.md` for 5-minute setup
2. Get Gmail App Password
3. Update `.env` file
4. Test registration flow
5. Enjoy secure authentication! 🎉
