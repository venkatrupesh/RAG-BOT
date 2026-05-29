# Email Verification Setup Guide

## Why Email Verification?

Email verification adds an important security layer:
- ✅ Prevents fake account creation
- ✅ Verifies user identity
- ✅ Reduces spam and abuse
- ✅ Ensures valid contact information
- ✅ Professional user experience

## Setup Instructions

### Step 1: Get Gmail App Password

1. **Go to your Google Account**: https://myaccount.google.com/
2. **Enable 2-Step Verification** (if not already enabled):
   - Go to Security → 2-Step Verification
   - Follow the setup process
3. **Create App Password**:
   - Go to Security → 2-Step Verification → App passwords
   - Select app: "Mail"
   - Select device: "Windows Computer"
   - Click "Generate"
   - **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

### Step 2: Update .env File

Open your `.env` file and add these lines:

```env
# API Keys
GROQ_API_KEY=your_existing_groq_key_here

# Email Configuration (for verification)
SENDER_EMAIL=your.email@gmail.com
SENDER_PASSWORD=your_16_char_app_password_here
```

**Example:**
```env
GROQ_API_KEY=your_groq_api_key_here
SENDER_EMAIL=your.email@gmail.com
SENDER_PASSWORD=your_app_password_here
```

### Step 3: Test Email Verification

1. Run the app: `streamlit run ui\app.py`
2. Go to "Create Account" tab
3. Fill in username, email, password
4. Click "📧 Send Verification Code"
5. Check your email for the 6-digit code
6. Enter the code and click "✅ Verify"
7. Account created! Sign in with your credentials

## How It Works

### Registration Flow:

```
1. User enters: username, email, password
   ↓
2. Click "Send Verification Code"
   ↓
3. System generates 6-digit code
   ↓
4. Email sent to user's inbox
   ↓
5. User enters code from email
   ↓
6. Click "Verify"
   ↓
7. Code validated (expires in 10 minutes)
   ↓
8. Account created ✅
```

### Security Features:

- **6-digit random code**: Hard to guess
- **10-minute expiry**: Prevents code reuse
- **One-time use**: Code deleted after verification
- **Email validation**: Ensures real email address
- **Duplicate prevention**: Checks existing usernames/emails

## Troubleshooting

### Error: "Email configuration missing"

**Solution**: Add `SENDER_EMAIL` and `SENDER_PASSWORD` to `.env` file

### Error: "Email authentication failed"

**Possible causes:**
1. Wrong app password
2. 2-Step Verification not enabled
3. Using regular password instead of app password

**Solution**: 
- Generate a new app password from Google Account
- Make sure to use the 16-character app password, not your regular Gmail password

### Error: "Failed to send email"

**Possible causes:**
1. No internet connection
2. Gmail SMTP blocked by firewall
3. Invalid email format

**Solution**:
- Check internet connection
- Try different network
- Verify email format is correct

### Code not received

**Check:**
1. Spam/Junk folder
2. Email address spelling
3. Wait 1-2 minutes (sometimes delayed)

### Code expired

**Solution**: 
- Click "🔙 Back" button
- Request a new code
- Codes expire after 10 minutes

## Alternative: Disable Email Verification

If you don't want email verification (for testing/development):

1. Open `ui\app.py`
2. Find the signup section
3. Replace the verification flow with simple registration:

```python
if st.button("Create Account", key="reg_btn", use_container_width=True):
    if new_user and new_email and new_pass:
        ok, msg = register_user(new_user, new_pass, new_email)
        if ok:
            st.success(msg)
        else:
            st.error(msg)
    else:
        st.warning("Please fill in all fields.")
```

## Files Involved

- `ui\app.py` - Main app with verification UI
- `utils\email_service.py` - Email sending logic
- `utils\verification_store.py` - Code storage and validation
- `.env` - Email credentials (DO NOT COMMIT)
- `verification_codes.json` - Temporary code storage (auto-created)

## Security Best Practices

1. **Never commit .env file** to Git
2. **Use app passwords**, not regular passwords
3. **Keep codes short-lived** (10 minutes)
4. **Delete codes after use**
5. **Validate email format**
6. **Check for duplicate accounts**

## Production Deployment

For production, consider:
- Using a dedicated email service (SendGrid, AWS SES, Mailgun)
- Storing codes in a database instead of JSON
- Adding rate limiting (max 3 codes per hour)
- Logging verification attempts
- Adding CAPTCHA to prevent bots

## Support

If you still have issues:
1. Check all steps above
2. Verify .env file format
3. Test with a different email
4. Check Python version (3.8+)
5. Ensure all dependencies installed: `pip install -r requirements.txt`

---

**Note**: Gmail allows 100 emails per day for free accounts. For high-volume applications, use a professional email service.
