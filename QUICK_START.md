# Quick Start Guide - Email Verification

## ⚡ Fast Setup (5 minutes)

### 1. Get Gmail App Password

**Quick Link**: https://myaccount.google.com/apppasswords

**Steps:**
1. Click the link above
2. Sign in to your Google Account
3. If prompted, enable 2-Step Verification first
4. Select "Mail" and "Windows Computer"
5. Click "Generate"
6. **Copy the 16-character password** (looks like: `abcd efgh ijkl mnop`)

### 2. Update .env File

Open `.env` file and replace these lines:

```env
SENDER_EMAIL=your.email@gmail.com          ← Replace with your Gmail
SENDER_PASSWORD=your_16_char_app_password  ← Replace with app password
```

**Example:**
```env
SENDER_EMAIL=rushikesh@gmail.com
SENDER_PASSWORD=abcd efgh ijkl mnop
```

### 3. Run the App

```bash
streamlit run ui\app.py
```

### 4. Test Registration

1. Go to "Create Account" tab
2. Enter username, email, password
3. Click "📧 Send Verification Code"
4. Check your email inbox
5. Enter the 6-digit code
6. Click "✅ Verify"
7. Done! ✅

## 🎯 What You Get

- ✅ **Secure Registration**: Email verification prevents fake accounts
- ✅ **Professional UX**: Clean, modern interface
- ✅ **6-digit Codes**: Sent instantly to user's email
- ✅ **10-minute Expiry**: Codes expire for security
- ✅ **One-time Use**: Each code works only once
- ✅ **Duplicate Prevention**: Checks existing users/emails

## 🚨 Common Issues

### "Email configuration missing"
→ Add `SENDER_EMAIL` and `SENDER_PASSWORD` to `.env`

### "Email authentication failed"
→ Use **App Password**, not your regular Gmail password

### Code not received
→ Check spam folder, wait 1-2 minutes

### Code expired
→ Click "Back" and request a new code

## 📖 Full Documentation

See `EMAIL_SETUP_GUIDE.md` for detailed instructions and troubleshooting.

## 🔒 Security Notes

- Never share your app password
- Never commit `.env` file to Git
- Codes expire in 10 minutes
- Each code is single-use only

---

**Need Help?** Check `EMAIL_SETUP_GUIDE.md` for detailed troubleshooting.
