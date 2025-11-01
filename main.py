"""
Main entry point for AutoMail script.
Orchestrates the workflow: read CSV, configure SMTP, send emails.
"""

import sys
import argparse
from config import CSV_FILE_PATH, IMAGE_FILE_PATH, COLUMN_MAP, EMAILS_PER_HOUR, DELAY_SECONDS
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
    parser.add_argument('--test-rate', type=int, metavar='N',
                       help='Override emails per hour for testing (e.g., --test-rate 3600 for 1 email/sec)')
    parser.add_argument('--csv', type=str, metavar='PATH',
                       help='Override CSV file path')
    args = parser.parse_args()
    
    print("=" * 50)
    print("AutoMail - Email Automation Script")
    print("=" * 50)
    print()
    
    # Override CSV path if provided
    csv_path = args.csv if args.csv else CSV_FILE_PATH
    
    # Calculate rate limiting (override if test-rate provided)
    if args.test_rate:
        test_emails_per_hour = args.test_rate
        test_delay = 3600 / test_emails_per_hour
        print(f"TEST MODE: Using {test_emails_per_hour} emails/hour ({test_delay:.1f}s delay)")
        print()
    else:
        test_emails_per_hour = EMAILS_PER_HOUR
        test_delay = DELAY_SECONDS
    
    # Step 1: Read customers from CSV
    print(f"Step 1: Reading customers from {csv_path}...")
    customers = read_customers(csv_path, COLUMN_MAP)
    
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
    print(f"Ready to send {len(customers)} emails at a rate of {test_emails_per_hour} per hour")
    print(f"Estimated time: {len(customers) * test_delay / 3600:.2f} hours ({len(customers) * test_delay / 60:.1f} minutes)")
    
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
    
    # Pass custom delay if test mode is active
    stats = send_emails(customers, smtp_config, build_email, IMAGE_FILE_PATH, custom_delay=test_delay if args.test_rate else None)
    
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

