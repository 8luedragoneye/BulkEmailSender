"""Test German email content"""
from email_builder import build_email

# Test different genders
test_cases = [
    {'email': 'test@example.com', 'name': 'Mustermann', 'gender': 'Mann'},
    {'email': 'test@example.com', 'name': 'Schmidt', 'gender': 'Frau'},
    {'email': 'test@example.com', 'name': 'Weber', 'gender': ''},
]

sender = 'test@example.com'

for customer in test_cases:
    msg = build_email(customer, None, sender)
    print(f"\nGender: '{customer['gender']}'")
    print(f"Subject: {msg['Subject']}")
    
    # Extract text body
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True).decode('utf-8')
            print(f"Body:\n{body[:200]}...")  # First 200 chars
            break

