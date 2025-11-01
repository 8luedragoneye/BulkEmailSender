"""
Main entry point for AutoMail script.
Orchestrates the workflow: read CSV, configure SMTP, send emails.
"""

import sys
import argparse
from config import CSV_FILE_PATH, IMAGE_FILE_PATH, COLUMN_MAP
from csv_reader import read_customers
from smtp_config import get_smtp_config
from email_builder import build_email
from sender import send_emails


def main():
    """Main function that orchestrates the email sending workflow."""
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='AutoMail - Email Automation Script')
    parser.add_argument('--yes', '-y', action='store_true', 
                       help='Skip confirmation prompt and proceed with sending')
    args = parser.parse_args()
    
    print("=" * 50)
    print("AutoMail - Email Automation Script")
    print("=" * 50)
    print()
    
    # Step 1: Read customers from CSV
    print(f"Step 1: Reading customers from {CSV_FILE_PATH}...")
    customers = read_customers(CSV_FILE_PATH, COLUMN_MAP)
    
    if not customers:
        print("No customers found. Exiting.")
        sys.exit(1)
    
    print(f"Found {len(customers)} customers")
    print()
    
    # Step 2: Get SMTP configuration
    print("Step 2: Loading SMTP configuration...")
    smtp_config = get_smtp_config()
    
    # Validate configuration
    if smtp_config['username'] == 'your_email@gmail.com' or smtp_config['password'] == 'your_app_password':
        print("Warning: Please configure your email credentials in smtp_config.py or set EMAIL_USERNAME and EMAIL_PASSWORD environment variables")
    
    print(f"SMTP server: {smtp_config['host']}:{smtp_config['port']}")
    print()
    
    # Step 3: Confirm before sending
    print(f"Ready to send {len(customers)} emails at a rate of 100 per hour")
    print(f"Estimated time: {len(customers) * 36 / 3600:.1f} hours")
    
    if args.yes:
        print("Auto-confirming (--yes flag provided)")
    else:
        response = input("Proceed with sending? (yes/no): ")
        
        if response.lower() not in ['yes', 'y']:
            print("Cancelled.")
            sys.exit(0)
    
    print()
    
    # Step 4: Send emails
    print("Step 3: Sending emails...")
    print("-" * 50)
    
    stats = send_emails(customers, smtp_config, build_email, IMAGE_FILE_PATH)
    
    # Step 5: Print summary
    print()
    print("-" * 50)
    print("Summary:")
    print(f"  Total: {stats['total']}")
    print(f"  Sent: {stats['sent']}")
    print(f"  Failed: {stats['failed']}")
    print("=" * 50)


if __name__ == '__main__':
    main()

