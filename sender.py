"""
Email sending module with rate limiting.
"""

import smtplib
import time
from email.utils import formatdate
from collections import deque


def send_emails(customers, smtp_config, build_func, image_path, custom_delay=None):
    """
    Send emails to customers with rate limiting (100 emails per hour).
    
    Args:
        customers: List of customer dictionaries
        smtp_config: Dictionary with SMTP settings (host, port, username, password)
        build_func: Function that builds email (takes customer, image_path, sender_email)
        image_path: Path to image file
        custom_delay: Optional custom delay in seconds (deprecated, rate limit is enforced instead)
    
    Returns:
        Dictionary with statistics: {'sent': count, 'failed': count, 'total': count}
    """
    stats = {
        'sent': 0,
        'failed': 0,
        'total': len(customers)
    }
    
    # Rate limiting: 100 emails per hour
    from config import EMAILS_PER_HOUR
    RATE_LIMIT = EMAILS_PER_HOUR  # emails per hour
    HOUR_IN_SECONDS = 3600
    MIN_DELAY = HOUR_IN_SECONDS / RATE_LIMIT  # minimum seconds between emails (36s for 100/hour)
    
    # Track timestamps of sent emails for rate limiting
    sent_timestamps = deque()
    
    sender_email = smtp_config['username']
    
    try:
        # Connect to SMTP server
        print(f"Connecting to {smtp_config['host']}...")
        server = smtplib.SMTP(smtp_config['host'], smtp_config['port'])
        server.starttls()  # Enable encryption
        server.login(smtp_config['username'], smtp_config['password'])
        print("Connected successfully!")
        print(f"Rate limit: {RATE_LIMIT} emails per hour (minimum {MIN_DELAY:.1f}s between emails)")
        
        # Send emails to each customer
        start_time = time.time()
        for i, customer in enumerate(customers, 1):
            try:
                email_start = time.time()
                
                # Enforce rate limit: ensure we don't exceed 100 emails in the last hour
                current_time = time.time()
                
                # Remove timestamps older than 1 hour
                while sent_timestamps and current_time - sent_timestamps[0] >= HOUR_IN_SECONDS:
                    sent_timestamps.popleft()
                
                # If we've already sent 100 emails in the last hour, wait until one expires
                if len(sent_timestamps) >= RATE_LIMIT:
                    oldest_timestamp = sent_timestamps[0]
                    wait_time = (oldest_timestamp + HOUR_IN_SECONDS) - current_time + 0.1  # small buffer
                    if wait_time > 0:
                        print(f"\nRate limit reached: {RATE_LIMIT} emails sent in last hour.")
                        print(f"Waiting {wait_time:.1f} seconds to maintain limit...", end='', flush=True)
                        time.sleep(wait_time)
                        current_time = time.time()
                        # Clean up old timestamps again after waiting
                        while sent_timestamps and current_time - sent_timestamps[0] >= HOUR_IN_SECONDS:
                            sent_timestamps.popleft()
                        print(" Continuing...")
                
                # Ensure minimum delay since last email (if not first email)
                if sent_timestamps:
                    time_since_last = current_time - sent_timestamps[-1]
                    if time_since_last < MIN_DELAY:
                        wait_time = MIN_DELAY - time_since_last
                        print(f"Waiting {wait_time:.1f} seconds to maintain rate limit...", end='', flush=True)
                        time.sleep(wait_time)
                        current_time = time.time()
                
                # Build email
                msg = build_func(customer, image_path, sender_email)
                
                # Send email
                server.send_message(msg)
                
                # Record timestamp of successful send
                sent_time = time.time()
                sent_timestamps.append(sent_time)
                
                email_duration = sent_time - email_start
                stats['sent'] += 1
                
                emails_in_last_hour = len([ts for ts in sent_timestamps if sent_time - ts < HOUR_IN_SECONDS])
                # Format customer name from vorname/nachname
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
                print(f"[{i}/{stats['total']}] Sent to {display_name} ({customer['email']}) - took {email_duration:.2f}s (rate: {emails_in_last_hour}/{RATE_LIMIT} emails/hour)")
            
            except Exception as e:
                stats['failed'] += 1
                print(f"Error sending to {customer.get('email', 'unknown')}: {e}")
                # Continue to next customer
        
        # Close connection
        server.quit()
        total_duration = time.time() - start_time
        avg_time_per_email = total_duration / stats['total'] if stats['total'] > 0 else 0
        print(f"\nEmail sending complete!")
        print(f"Total time: {total_duration:.1f} seconds ({total_duration/60:.2f} minutes)")
        print(f"Average time per email: {avg_time_per_email:.1f} seconds")
        
    except smtplib.SMTPAuthenticationError:
        print("Error: Authentication failed. Check your username and password.")
        stats['failed'] = stats['total']
    except Exception as e:
        print(f"Error connecting to SMTP server: {e}")
        stats['failed'] = stats['total']
    
    return stats

