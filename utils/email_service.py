# utils/email_service.py

import os
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def generate_verification_code():
    """Generate a 6-digit verification code"""
    return str(random.randint(100000, 999999))

def get_code_expiry():
    """Get expiry time (10 minutes from now)"""
    return datetime.now() + timedelta(minutes=10)

def send_verification_email(to_email, code):
    """
    Send verification code via email
    Returns: (success: bool, message: str)
    """
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    
    # Check if email credentials are configured
    if not sender_email or not sender_password:
        return False, "Email configuration missing. Please set SENDER_EMAIL and SENDER_PASSWORD in .env file"
    
    # Check if using placeholder values
    if sender_email == "your.email@gmail.com" or sender_password == "your_16_char_app_password_here":
        return False, "Please update .env with your real Gmail credentials. See FIX_EMAIL_ERROR.md for help."
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = "InterviewAI - Email Verification Code"
        
        # Email body
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f9fafb;">
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <h1 style="color: #111827; margin-bottom: 10px;">💬 InterviewAI</h1>
                <h2 style="color: #374151; margin-bottom: 20px;">Email Verification</h2>
                <p style="color: #6b7280; font-size: 16px; line-height: 1.6;">
                    Thank you for signing up! Please use the verification code below to complete your registration:
                </p>
                <div style="background: #f3f4f6; padding: 20px; border-radius: 8px; text-align: center; margin: 30px 0;">
                    <h1 style="color: #111827; font-size: 36px; letter-spacing: 8px; margin: 0;">{code}</h1>
                </div>
                <p style="color: #6b7280; font-size: 14px;">
                    This code will expire in <strong>10 minutes</strong>.
                </p>
                <p style="color: #9ca3af; font-size: 13px; margin-top: 30px; border-top: 1px solid #e5e7eb; padding-top: 20px;">
                    If you didn't request this code, please ignore this email.
                </p>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Send email using Gmail SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        return True, "Verification code sent successfully!"
        
    except smtplib.SMTPAuthenticationError:
        return False, "Email authentication failed. Please check your email and app password."
    except smtplib.SMTPException as e:
        return False, f"Failed to send email: {str(e)}"
    except Exception as e:
        return False, f"Error: {str(e)}"
