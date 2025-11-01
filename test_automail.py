"""
Test script for AutoMail functionality.
Tests CSV reading, email building, and configuration without sending emails.
"""

import os
import sys
from config import CSV_FILE_PATH, IMAGE_FILE_PATH, COLUMN_MAP, DELAY_SECONDS, EMAILS_PER_HOUR
from csv_reader import read_customers
from smtp_config import get_smtp_config
from email_builder import build_email


def test_csv_reading():
    """Test CSV reading functionality."""
    print("=" * 50)
    print("TEST 1: CSV Reading")
    print("=" * 50)
    
    test_csv = 'test_customers.csv'
    
    if not os.path.exists(test_csv):
        print(f"[FAIL] Test CSV file '{test_csv}' not found")
        return False
    
    customers = read_customers(test_csv, COLUMN_MAP)
    
    if not customers:
        print("[FAIL] No customers read from CSV")
        return False
    
    print(f"[PASS] Successfully read {len(customers)} customers")
    
    # Check structure
    if len(customers) > 0:
        sample = customers[0]
        print(f"   Sample customer: {sample}")
        
        required_fields = ['email', 'name', 'gender']
        for field in required_fields:
            if field not in sample:
                print(f"[FAIL] Missing field '{field}' in customer data")
                return False
    
    print("[PASS] CSV structure validation passed")
    print()
    return True


def test_smtp_config():
    """Test SMTP configuration loading."""
    print("=" * 50)
    print("TEST 2: SMTP Configuration")
    print("=" * 50)
    
    smtp_config = get_smtp_config()
    
    required_keys = ['host', 'port', 'username', 'password']
    for key in required_keys:
        if key not in smtp_config:
            print(f"[FAIL] Missing SMTP config key: {key}")
            return False
    
    print(f"[PASS] SMTP configuration loaded")
    print(f"   Host: {smtp_config['host']}")
    print(f"   Port: {smtp_config['port']}")
    print(f"   Username: {smtp_config['username']}")
    print()
    return True


def test_email_building():
    """Test email message building."""
    print("=" * 50)
    print("TEST 3: Email Building")
    print("=" * 50)
    
    # Test customer data
    test_customer = {
        'email': 'test@example.com',
        'name': 'Test User',
        'gender': 'Male'
    }
    
    sender_email = 'sender@example.com'
    
    try:
        # Build email without image (image path can be None or non-existent)
        msg = build_email(test_customer, None, sender_email)
        
        # Validate message structure
        if msg['To'] != test_customer['email']:
            print(f"[FAIL] Incorrect recipient: {msg['To']}")
            return False
        
        if msg['From'] != sender_email:
            print(f"[FAIL] Incorrect sender: {msg['From']}")
            return False
        
        if not msg['Subject']:
            print(f"[FAIL] Missing subject")
            return False
        
        print("[PASS] Email message built successfully")
        print(f"   To: {msg['To']}")
        print(f"   From: {msg['From']}")
        print(f"   Subject: {msg['Subject']}")
        print()
        
        # Test with non-existent image (should not crash)
        msg2 = build_email(test_customer, 'nonexistent.png', sender_email)
        print("[PASS] Email building handles missing image gracefully")
        print()
        
        return True
    
    except Exception as e:
        print(f"[FAIL] Error building email: {e}")
        return False


def test_configuration():
    """Test configuration values."""
    print("=" * 50)
    print("TEST 4: Configuration")
    print("=" * 50)
    
    # Test rate limiting calculation
    expected_delay = 3600 / EMAILS_PER_HOUR
    if abs(DELAY_SECONDS - expected_delay) > 0.1:
        print(f"[FAIL] Delay calculation incorrect: {DELAY_SECONDS} != {expected_delay}")
        return False
    
    print(f"[PASS] Rate limiting: {EMAILS_PER_HOUR} emails/hour = {DELAY_SECONDS:.1f}s delay")
    
    # Test column map
    if not COLUMN_MAP or 'email' not in COLUMN_MAP:
        print("[FAIL] Invalid column mapping")
        return False
    
    print(f"[PASS] Column mapping configured: {COLUMN_MAP}")
    print()
    return True


def test_module_imports():
    """Test that all modules can be imported."""
    print("=" * 50)
    print("TEST 5: Module Imports")
    print("=" * 50)
    
    try:
        from csv_reader import read_customers
        from smtp_config import get_smtp_config
        from email_builder import build_email
        from sender import send_emails
        print("[PASS] All modules imported successfully")
        print()
        return True
    except ImportError as e:
        print(f"[FAIL] Import error: {e}")
        print("   Make sure all required packages are installed:")
        print("   pip install -r requirements.txt")
        print()
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("AutoMail Test Suite")
    print("=" * 50)
    print()
    
    results = []
    
    results.append(("Module Imports", test_module_imports()))
    results.append(("Configuration", test_configuration()))
    results.append(("CSV Reading", test_csv_reading()))
    results.append(("SMTP Config", test_smtp_config()))
    results.append(("Email Building", test_email_building()))
    
    # Summary
    print("=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("[PASS] All tests passed!")
        return 0
    else:
        print("[FAIL] Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())

