"""
Quick test script to send a test email without confirmation prompt.
"""

import sys
from config import CSV_FILE_PATH, IMAGE_FILE_PATH, COLUMN_MAP
from csv_reader import read_customers
from smtp_config import get_smtp_config
from email_builder import build_email
from sender import send_emails


def main():
    """Send test email without confirmation."""
    
    print("=" * 50)
    print("AutoMail - Test Email")
    print("=" * 50)
    print()
    
    # Step 1: Read customers from CSV
    print(f"Step 1: Reading customers from {CSV_FILE_PATH}...")
    customers = read_customers(CSV_FILE_PATH, COLUMN_MAP)
    
    if not customers:
        print("No customers found. Exiting.")
        sys.exit(1)
    
    print(f"Found {len(customers)} customer(s)")
    print()
    
    # Step 2: Get SMTP configuration
    print("Step 2: Loading SMTP configuration...")
    smtp_config = get_smtp_config()
    
    # Validate configuration
    if smtp_config['username'] == 'your_email@gmail.com' or smtp_config['password'] == 'your_app_password':
        print("Warning: Please configure your email credentials in smtp_config.py or set EMAIL_USERNAME and EMAIL_PASSWORD environment variables")
        sys.exit(1)
    
    print(f"SMTP server: {smtp_config['host']}:{smtp_config['port']}")
    print()
    
    # Step 3: Send emails (no confirmation needed for test)
    print(f"Step 3: Sending test email to {customers[0]['email']}...")
    print("-" * 50)
    
    stats = send_emails(customers, smtp_config, build_email, IMAGE_FILE_PATH)
    
    # Step 4: Print summary
    print()
    print("-" * 50)
    print("Summary:")
    print(f"  Total: {stats['total']}")
    print(f"  Sent: {stats['sent']}")
    print(f"  Failed: {stats['failed']}")
    print("=" * 50)
    
    if stats['sent'] > 0:
        print("Test email sent successfully!")
        return 0
    else:
        print("Test email failed to send.")
        return 1


if __name__ == '__main__':
    sys.exit(main())

