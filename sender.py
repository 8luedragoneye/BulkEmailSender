"""
Email sending module with rate limiting.
"""

import smtplib
import time
from email.utils import formatdate


def send_emails(customers, smtp_config, build_func, image_path):
    """
    Send emails to customers with rate limiting.
    
    Args:
        customers: List of customer dictionaries
        smtp_config: Dictionary with SMTP settings (host, port, username, password)
        build_func: Function that builds email (takes customer, image_path, sender_email)
        image_path: Path to image file
    
    Returns:
        Dictionary with statistics: {'sent': count, 'failed': count, 'total': count}
    """
    stats = {
        'sent': 0,
        'failed': 0,
        'total': len(customers)
    }
    
    # Calculate delay between emails (in seconds)
    from config import DELAY_SECONDS
    delay = DELAY_SECONDS
    
    sender_email = smtp_config['username']
    
    try:
        # Connect to SMTP server
        print(f"Connecting to {smtp_config['host']}...")
        server = smtplib.SMTP(smtp_config['host'], smtp_config['port'])
        server.starttls()  # Enable encryption
        server.login(smtp_config['username'], smtp_config['password'])
        print("Connected successfully!")
        
        # Send emails to each customer
        for i, customer in enumerate(customers, 1):
            try:
                # Build email
                msg = build_func(customer, image_path, sender_email)
                
                # Send email
                server.send_message(msg)
                
                stats['sent'] += 1
                print(f"[{i}/{stats['total']}] Sent to {customer.get('name', 'N/A')} ({customer['email']})")
                
                # Rate limiting: wait before next email (except for last one)
                if i < len(customers):
                    print(f"Waiting {delay:.1f} seconds before next email...")
                    time.sleep(delay)
            
            except Exception as e:
                stats['failed'] += 1
                print(f"Error sending to {customer.get('email', 'unknown')}: {e}")
                # Continue to next customer
        
        # Close connection
        server.quit()
        print("\nEmail sending complete!")
        
    except smtplib.SMTPAuthenticationError:
        print("Error: Authentication failed. Check your username and password.")
        stats['failed'] = stats['total']
    except Exception as e:
        print(f"Error connecting to SMTP server: {e}")
        stats['failed'] = stats['total']
    
    return stats

