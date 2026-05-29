# Fix "Email Authentication Failed" Error

## Problem
You're seeing: **"Email authentication failed. Please check your email and app password."**

## Cause
The `.env` file still has placeholder values instead of your real Gmail credentials.

---

## Solution (5 Minutes)

### Step 1: Get Gmail App Password (3 minutes)

1. **Open this link**: https://myaccount.google.com/apppasswords
   
2. **Sign in** to your Google Account

3. **Enable 2-Step Verification** (if not already enabled):
   - You'll see a prompt if it's not enabled
   - Follow the steps to enable it
   - This is required for app passwords

4. **Create App Password**:
   - After 2-Step is enabled, you'll see "App passwords"
   - Click "Select app" → Choose **"Mail"**
   - Click "Select device" → Choose **"Windows Computer"**
   - Click **"Generate"**

5. **Copy the password**:
   - You'll see a 16-character password like: `abcd efgh ijkl mnop`
   - **Copy this password** (you'll need it in Step 2)

### Step 2: Update .env File (2 minutes)

1. **Open** the file: `c:\Users\rushi\OneDrive\Desktop\RAG-CHATBOT\.env`

2. **Replace these lines**:
   ```env
   SENDER_EMAIL=your.email@gmail.com
   SENDER_PASSWORD=your_16_char_app_password_here
   ```

3. **With your actual values**:
   ```env
   SENDER_EMAIL=rushikesh@gmail.com
   SENDER_PASSWORD=abcd efgh ijkl mnop
   ```
   
   ⚠️ **Important**:
   - Use your **actual Gmail address**
   - Use the **16-character app password** (not your regular Gmail password)
   - Keep the spaces in the app password (e.g., `abcd efgh ijkl mnop`)

4. **Save the file** (Ctrl + S)

### Step 3: Restart the App (30 seconds)

1. **Stop the app** (if running):
   - Press `Ctrl + C` in the terminal

2. **Start it again**:
   ```bash
   streamlit run ui\app.py
   ```

3. **Test registration**:
   - Go to "Create Account" tab
   - Fill in details
   - Click "Send Verification Code"
   - Should work now! ✅

---

## Example .env File

Here's what your `.env` should look like (with YOUR values):

```env
# API Keys - DO NOT COMMIT THIS FILE
GROQ_API_KEY=your_groq_api_key_here

# Email Configuration (for email verification)
SENDER_EMAIL=your.email@gmail.com
SENDER_PASSWORD=your_app_password_here
```

---

## Common Mistakes

### ❌ Wrong: Using regular Gmail password
```env
SENDER_PASSWORD=MyGmailPassword123
```
**Fix**: Use the 16-character app password from Google

### ❌ Wrong: Removing spaces from app password
```env
SENDER_PASSWORD=abcdefghijklmnop
```
**Fix**: Keep the spaces: `abcd efgh ijkl mnop`

### ❌ Wrong: Using placeholder values
```env
SENDER_EMAIL=your.email@gmail.com
SENDER_PASSWORD=your_16_char_app_password_here
```
**Fix**: Replace with your actual Gmail and app password

### ❌ Wrong: Not enabling 2-Step Verification
**Fix**: You MUST enable 2-Step Verification first

---

## Troubleshooting

### "I don't see App Passwords option"
**Reason**: 2-Step Verification not enabled
**Fix**: 
1. Go to: https://myaccount.google.com/security
2. Enable "2-Step Verification"
3. Then go back to: https://myaccount.google.com/apppasswords

### "App password not working"
**Check**:
- ✅ Did you copy the entire 16-character password?
- ✅ Did you keep the spaces?
- ✅ Did you save the `.env` file?
- ✅ Did you restart the app?

### "Still getting authentication error"
**Try**:
1. Generate a NEW app password
2. Delete the old one
3. Update `.env` with the new password
4. Restart the app

---

## Quick Test

After updating `.env`, test if it works:

```bash
# Stop the app (Ctrl + C)
# Start it again
streamlit run ui\app.py

# Then:
# 1. Go to "Create Account" tab
# 2. Enter test details
# 3. Click "Send Verification Code"
# 4. Check your email inbox
```

---

## Visual Guide

```
Step 1: Get App Password
┌─────────────────────────────────────┐
│ Google Account → Security           │
│ → 2-Step Verification (enable)      │
│ → App passwords                     │
│ → Select "Mail" + "Windows"         │
│ → Generate                          │
│ → Copy: abcd efgh ijkl mnop         │
└─────────────────────────────────────┘
              ↓
Step 2: Update .env
┌─────────────────────────────────────┐
│ Open: .env file                     │
│ Replace:                            │
│   SENDER_EMAIL=your@gmail.com       │
│   SENDER_PASSWORD=abcd efgh ijkl    │
│ Save file (Ctrl + S)                │
└─────────────────────────────────────┘
              ↓
Step 3: Restart App
┌─────────────────────────────────────┐
│ Stop: Ctrl + C                      │
│ Start: streamlit run ui\app.py      │
│ Test: Send verification code        │
│ Result: ✅ Email sent!              │
└─────────────────────────────────────┘
```

---

## Need Help?

If you're still stuck:

1. **Check your Gmail settings**:
   - Is 2-Step Verification enabled?
   - Did you generate an app password?

2. **Check your .env file**:
   - Are the values correct?
   - Did you save the file?

3. **Check the app**:
   - Did you restart it after updating .env?

4. **Try a different email**:
   - Some Gmail accounts have restrictions
   - Try with a different Gmail account

---

## Alternative: Disable Email Verification

If you can't get Gmail working right now, you can temporarily disable email verification:

See `DISABLE_EMAIL_VERIFICATION.md` for instructions.

---

**Once you update .env with your real Gmail credentials, it will work!** ✅
