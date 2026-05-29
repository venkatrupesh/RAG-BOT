# Gmail Setup - Quick Visual Guide

## 🚀 Fix "Email Authentication Failed" in 3 Steps

---

## Step 1: Get Gmail App Password (2 minutes)

### 1.1 Open Google Account
```
Click this link: https://myaccount.google.com/apppasswords
```

### 1.2 Enable 2-Step Verification (if needed)
```
If you see "2-Step Verification is off":
→ Click "Get Started"
→ Follow the steps to enable it
→ This is required for app passwords
```

### 1.3 Generate App Password
```
After 2-Step is enabled:
→ You'll see "App passwords"
→ Click "Select app" → Choose "Mail"
→ Click "Select device" → Choose "Windows Computer"  
→ Click "Generate"
```

### 1.4 Copy the Password
```
You'll see something like:

┌─────────────────────────────────┐
│  Your app password:             │
│                                 │
│  abcd efgh ijkl mnop            │
│                                 │
│  [Copy] [Done]                  │
└─────────────────────────────────┘

Click "Copy" or manually copy it
```

---

## Step 2: Update .env File (1 minute)

### 2.1 Open .env File
```
Location: c:\Users\rushi\OneDrive\Desktop\RAG-CHATBOT\.env
```

### 2.2 Find These Lines
```env
SENDER_EMAIL=your.email@gmail.com
SENDER_PASSWORD=your_16_char_app_password_here
```

### 2.3 Replace with Your Values
```env
SENDER_EMAIL=rushikesh@gmail.com
SENDER_PASSWORD=abcd efgh ijkl mnop
```

**Replace**:
- `rushikesh@gmail.com` → Your actual Gmail address
- `abcd efgh ijkl mnop` → The app password you copied

### 2.4 Save the File
```
Press: Ctrl + S
```

---

## Step 3: Restart the App (30 seconds)

### 3.1 Stop the App
```
In the terminal where Streamlit is running:
Press: Ctrl + C
```

### 3.2 Start Again
```bash
streamlit run ui\app.py
```

### 3.3 Test It
```
1. Go to "Create Account" tab
2. Fill in your details
3. Click "Send Verification Code"
4. ✅ Should work now!
5. Check your email for the code
```

---

## Visual Example

### Before (Not Working):
```env
# .env file
SENDER_EMAIL=your.email@gmail.com          ❌ Placeholder
SENDER_PASSWORD=your_16_char_app_password  ❌ Placeholder
```

### After (Working):
```env
# .env file
SENDER_EMAIL=rushikesh@gmail.com           ✅ Your Gmail
SENDER_PASSWORD=abcd efgh ijkl mnop        ✅ App Password
```

---

## Common Issues

### Issue 1: "I don't see App Passwords"
**Reason**: 2-Step Verification not enabled
**Fix**: 
1. Go to https://myaccount.google.com/security
2. Enable "2-Step Verification"
3. Then go to https://myaccount.google.com/apppasswords

### Issue 2: "Authentication still failing"
**Check**:
- ✅ Did you use the app password (not your regular password)?
- ✅ Did you keep the spaces in the app password?
- ✅ Did you save the .env file?
- ✅ Did you restart the app?

### Issue 3: "App password not working"
**Try**:
1. Delete the old app password in Google Account
2. Generate a NEW app password
3. Update .env with the new password
4. Restart the app

---

## Screenshot Guide

### Step 1: Google Account Security
```
https://myaccount.google.com/security

┌─────────────────────────────────────────┐
│ Security                                │
│                                         │
│ ✅ 2-Step Verification: ON             │
│    → App passwords                      │
│                                         │
└─────────────────────────────────────────┘
```

### Step 2: Generate App Password
```
https://myaccount.google.com/apppasswords

┌─────────────────────────────────────────┐
│ App passwords                           │
│                                         │
│ Select app:  [Mail ▼]                  │
│ Select device: [Windows Computer ▼]    │
│                                         │
│ [Generate]                              │
└─────────────────────────────────────────┘
```

### Step 3: Copy Password
```
┌─────────────────────────────────────────┐
│ Your app password for Windows Computer │
│                                         │
│ abcd efgh ijkl mnop                     │
│                                         │
│ [Copy]  [Done]                          │
└─────────────────────────────────────────┘
```

---

## Quick Checklist

- [ ] Opened https://myaccount.google.com/apppasswords
- [ ] Enabled 2-Step Verification (if needed)
- [ ] Generated app password for "Mail"
- [ ] Copied the 16-character password
- [ ] Opened .env file
- [ ] Replaced SENDER_EMAIL with my Gmail
- [ ] Replaced SENDER_PASSWORD with app password
- [ ] Saved .env file (Ctrl + S)
- [ ] Stopped the app (Ctrl + C)
- [ ] Started the app again
- [ ] Tested "Send Verification Code"
- [ ] ✅ It works!

---

## Need More Help?

Read these files:
- `FIX_EMAIL_ERROR.md` - Detailed troubleshooting
- `EMAIL_SETUP_GUIDE.md` - Complete setup guide
- `QUICK_START.md` - 5-minute setup

---

**After following these steps, email verification will work!** ✅
