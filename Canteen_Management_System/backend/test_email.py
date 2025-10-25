#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_cms.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_sending():
    """Test email sending with current configuration"""
    
    print("Testing email configuration...")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    # Test email
    test_email = "birthdaywisher2025@gmail.com"  # Send to yourself first
    
    try:
        result = send_mail(
            subject="Test Email - MITS Canteen",
            message="This is a test email to verify email configuration is working.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False
        )
        
        print(f"✅ Email sent successfully! Result: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    test_email_sending()