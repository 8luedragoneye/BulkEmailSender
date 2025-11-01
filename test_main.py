"""
Test the main script workflow without requiring user input or actual email sending.
"""

import sys
from config import CSV_FILE_PATH, IMAGE_FILE_PATH, COLUMN_MAP
from csv_reader import read_customers
from smtp_config import get_smtp_config
from email_builder import build_email


def test_main_workflow():
    """Test the main workflow up to the sending step."""
    
    print("=" * 50)
    print("Testing Main Workflow")
    print("=" * 50)
    print()
    
    # Step 1: Read customers from CSV
    print(f"Step 1: Reading customers from {CSV_FILE_PATH}...")
    customers = read_customers(CSV_FILE_PATH, COLUMN_MAP)
    
    if not customers:
        print("[FAIL] No customers found.")
        return False
    
    print(f"[PASS] Found {len(customers)} customers")
    
    # Show sample customers
    print("\nSample customers:")
    for i, customer in enumerate(customers[:3], 1):
        vorname = customer.get('vorname', '')
        nachname = customer.get('nachname', '')
        if vorname and nachname:
            display_name = f"{vorname} {nachname}"
        elif vorname:
            display_name = vorname
        elif nachname:
            display_name = nachname
        else:
            display_name = 'N/A'
        print(f"  {i}. {display_name} ({customer.get('email', 'N/A')})")
    
    print()
    
    # Step 2: Get SMTP configuration
    print("Step 2: Loading SMTP configuration...")
    smtp_config = get_smtp_config()
    
    print(f"[PASS] SMTP configuration loaded")
    print(f"  Host: {smtp_config['host']}")
    print(f"  Port: {smtp_config['port']}")
    print(f"  Username: {smtp_config['username']}")
    print()
    
    # Step 3: Test email building
    print("Step 3: Testing email building...")
    test_customer = customers[0]
    sender_email = smtp_config['username']
    
    try:
        msg = build_email(test_customer, IMAGE_FILE_PATH, sender_email)
        vorname = test_customer.get('vorname', '')
        nachname = test_customer.get('nachname', '')
        display_name = f"{vorname} {nachname}".strip() if (vorname or nachname) else 'N/A'
        print(f"[PASS] Email built successfully for {display_name}")
        print(f"  To: {msg['To']}")
        print(f"  Subject: {msg['Subject']}")
        print()
    except Exception as e:
        print(f"[FAIL] Error building email: {e}")
        return False
    
    # Step 4: Calculate timing
    print("Step 4: Rate limiting calculation...")
    from config import DELAY_SECONDS, EMAILS_PER_HOUR
    estimated_hours = len(customers) * DELAY_SECONDS / 3600
    
    print(f"[PASS] Rate limiting configured")
    print(f"  Emails per hour: {EMAILS_PER_HOUR}")
    print(f"  Delay between emails: {DELAY_SECONDS:.1f} seconds")
    print(f"  Estimated time for {len(customers)} emails: {estimated_hours:.2f} hours")
    print()
    
    # Summary
    print("=" * 50)
    print("WORKFLOW TEST SUMMARY")
    print("=" * 50)
    print("[PASS] CSV reading: OK")
    print("[PASS] SMTP configuration: OK")
    print("[PASS] Email building: OK")
    print("[PASS] Rate limiting: OK")
    print()
    print(f"Ready to send {len(customers)} emails!")
    print("Note: Actual email sending requires configured SMTP credentials.")
    
    return True


if __name__ == '__main__':
    success = test_main_workflow()
    sys.exit(0 if success else 1)

