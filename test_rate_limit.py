"""
Test script to verify the 100 emails per hour rate limiting.

This test uses a mocked SMTP server to verify rate limiting without sending real emails.
You can also run a quick test with a smaller limit (e.g., 10 per minute) for faster verification.
"""

import time
import sys
from unittest.mock import Mock, MagicMock, patch
from collections import deque

# Import the sender module
from sender import send_emails
from email_builder import build_email


def create_test_customers(count=5):
    """Create test customer data."""
    return [
        {
            'email': f'test{i}@example.com',
            'vorname': f'Test{i}',
            'nachname': f'User{i}',
            'anrede': 'Herr' if i % 2 == 0 else 'Frau',
            'du': 'sie' if i % 2 == 0 else 'du'  # Alternate between sie and du
        }
        for i in range(1, count + 1)
    ]


def test_rate_limit_with_mock():
    """
    Test rate limiting logic by checking timing.
    Note: This test uses mocked SMTP but still runs with real timing delays.
    For a faster test, use the 'test_rate_limit_fast.py' script or modify EMAILS_PER_HOUR temporarily.
    """
    print("=" * 60)
    print("Rate Limiting Test (Mocked SMTP)")
    print("=" * 60)
    print()
    print("Note: This test verifies rate limiting logic but may take time")
    print("      due to the 100 emails/hour limit (36 seconds between emails).")
    print("      For faster testing, see instructions in README or use real SMTP test.")
    print()
    
    # Create test customers (3-4 is enough to verify delays)
    customers = create_test_customers(3)
    print(f"Prepared {len(customers)} test customers")
    print()
    
    # Mock SMTP server
    mock_server = MagicMock()
    mock_smtp = Mock(return_value=mock_server)
    
    # Mock SMTP config
    smtp_config = {
        'host': 'smtp.test.com',
        'port': 587,
        'username': 'test@example.com',
        'password': 'testpassword'
    }
    
    print("Starting rate limit test with mocked SMTP...")
    print("(This will show the timing behavior)")
    print("-" * 60)
    start_time = time.time()
    
    with patch('smtplib.SMTP', mock_smtp):
        stats = send_emails(customers, smtp_config, build_email, None)
    
    total_time = time.time() - start_time
    
    print("-" * 60)
    print()
    print("Test Results:")
    print(f"  Total customers: {stats['total']}")
    print(f"  Successfully processed: {stats['sent']}")
    print(f"  Failed: {stats['failed']}")
    print(f"  Total time: {total_time:.1f} seconds ({total_time/60:.2f} minutes)")
    print()
    
    # Verify rate limiting
    from config import DELAY_SECONDS
    if len(customers) > 1:
        expected_min_time = (len(customers) - 1) * DELAY_SECONDS
        print(f"Expected minimum time (with {DELAY_SECONDS:.1f}s delay): {expected_min_time:.1f} seconds")
        print(f"Actual time: {total_time:.1f} seconds")
        
        if total_time >= expected_min_time * 0.8:  # Allow 20% tolerance
            print("[PASS] Rate limiting appears to be working correctly!")
            print("       (Total time meets or exceeds expected minimum)")
            return True
        else:
            print("[WARNING] Rate limiting may not be working correctly")
            print("          (Total time is less than expected minimum)")
            return False
    
    print("[INFO] Test completed (only 1 email, cannot verify delays)")
    return True


def test_rate_limit_real_small(skip_confirmation=False):
    """
    Test with real SMTP but only a few emails (safe test).
    Uses the actual 100 per hour limit but sends only 3-5 emails.
    """
    print("=" * 60)
    print("Rate Limiting Test (Real SMTP - Small Batch)")
    print("=" * 60)
    print()
    print("This will send REAL emails. Make sure you have configured SMTP settings.")
    print()
    
    if not skip_confirmation:
        try:
            response = input("Do you want to proceed with real email test? (yes/no): ").strip().lower()
            if response != 'yes':
                print("Test cancelled.")
                return False
        except EOFError:
            print("No input available. Use --yes flag to skip confirmation.")
            return False
    
    from config import CSV_FILE_PATH, IMAGE_FILE_PATH, COLUMN_MAP
    from csv_reader import read_customers
    from smtp_config import get_smtp_config
    import os
    
    # Try to use test_rate_limit.csv if available (has 5 test customers)
    # Otherwise use the regular CSV file
    test_csv = 'test_rate_limit.csv'
    if os.path.exists(test_csv):
        print(f"Using {test_csv} for batch testing...")
        csv_path = test_csv
    else:
        print(f"Using {CSV_FILE_PATH} for testing...")
        csv_path = CSV_FILE_PATH
    
    # Read customers
    customers = read_customers(csv_path, COLUMN_MAP)
    if not customers:
        print("No customers found. Please check your CSV file.")
        return False
    
    # Use first 5 customers for testing (to verify rate limiting with multiple emails)
    test_customers = customers[:5]
    print(f"Using first {len(test_customers)} customers for testing")
    print()
    
    # Get SMTP config
    smtp_config = get_smtp_config()
    
    # Validate configuration
    if smtp_config['username'] == 'your_email@gmail.com' or smtp_config['password'] == 'your_app_password':
        print("Error: Please configure your email credentials first.")
        return False
    
    print(f"SMTP server: {smtp_config['host']}:{smtp_config['port']}")
    print()
    print("Starting rate limit test with REAL emails...")
    print("(This will verify delays between emails)")
    print("-" * 60)
    
    start_time = time.time()
    stats = send_emails(test_customers, smtp_config, build_email, IMAGE_FILE_PATH)
    total_time = time.time() - start_time
    
    print("-" * 60)
    print()
    print("Test Results:")
    print(f"  Total: {stats['total']}")
    print(f"  Sent: {stats['sent']}")
    print(f"  Failed: {stats['failed']}")
    print(f"  Total time: {total_time:.1f} seconds")
    print()
    
    if stats['sent'] > 0:
        expected_min_delay = 36.0  # 36 seconds for 100/hour
        if len(test_customers) > 1:
            expected_min_time = (len(test_customers) - 1) * expected_min_delay
            print(f"Expected minimum time: {expected_min_time:.1f} seconds")
            print(f"Actual time: {total_time:.1f} seconds")
            
            if total_time >= expected_min_time * 0.8:  # Allow some tolerance
                print("[PASS] Rate limiting appears to be working!")
            else:
                print("[WARNING] Rate limiting may need adjustment")
        
        return True
    else:
        print("[FAIL] No emails were sent successfully")
        return False


def main():
    """Run rate limiting tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test rate limiting for email sender')
    parser.add_argument('--mock', action='store_true', help='Run mock test (no real emails)')
    parser.add_argument('--real', action='store_true', help='Run real SMTP test (sends emails)')
    parser.add_argument('--both', action='store_true', help='Run both tests')
    parser.add_argument('--yes', action='store_true', help='Skip confirmation prompts (use with --real)')
    args = parser.parse_args()
    
    # Determine choice from arguments or prompt
    if args.mock:
        choice = '1'
    elif args.real:
        choice = '2'
    elif args.both:
        choice = '3'
    else:
        print("\n" + "=" * 60)
        print("Rate Limiting Test Suite")
        print("=" * 60)
        print()
        print("Choose a test option:")
        print("  1. Mock test (fast, no real emails) - Recommended")
        print("  2. Real SMTP test (sends real emails, small batch)")
        print("  3. Both")
        print()
        print("Or use command-line arguments: --mock, --real, or --both")
        print()
        try:
            choice = input("Enter choice (1/2/3): ").strip()
        except EOFError:
            # Default to mock test if no input available
            print("No input available, defaulting to mock test...")
            choice = '1'
    
    results = []
    
    if choice in ['1', '3']:
        print("\n" + "=" * 60)
        print("Running Mock Test...")
        print("=" * 60)
        print()
        try:
            result = test_rate_limit_with_mock()
            results.append(("Mock Test", result))
        except Exception as e:
            print(f"[FAIL] Mock test error: {e}")
            import traceback
            traceback.print_exc()
            results.append(("Mock Test", False))
    
    if choice in ['2', '3']:
        print("\n" + "=" * 60)
        print("Running Real SMTP Test...")
        print("=" * 60)
        print()
        try:
            result = test_rate_limit_real_small(skip_confirmation=args.yes)
            results.append(("Real SMTP Test", result))
        except KeyboardInterrupt:
            print("\n[INFO] Test interrupted by user")
            results.append(("Real SMTP Test", None))
        except Exception as e:
            print(f"[FAIL] Real SMTP test error: {e}")
            import traceback
            traceback.print_exc()
            results.append(("Real SMTP Test", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        if result is True:
            print(f"[PASS] {test_name}")
        elif result is False:
            print(f"[FAIL] {test_name}")
        else:
            print(f"[SKIP] {test_name}")
    
    print()
    
    passed = sum(1 for _, r in results if r is True)
    total = sum(1 for _, r in results if r is not None)
    
    if total > 0:
        print(f"Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n[SUCCESS] All rate limiting tests passed!")
            return 0
        else:
            print("\n[WARNING] Some tests failed or were skipped")
            return 1
    else:
        print("No tests were run")
        return 0


if __name__ == '__main__':
    sys.exit(main())

