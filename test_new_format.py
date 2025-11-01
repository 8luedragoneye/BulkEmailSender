"""Quick test to verify new CSV format with vorname/nachname/du fields."""

from config import COLUMN_MAP
from csv_reader import read_customers
from email_builder import build_email

# Read test customers
customers = read_customers('test_rate_limit.csv', COLUMN_MAP)
print(f"Loaded {len(customers)} customers\n")

# Test formal (sie) addressing
print("=" * 60)
print("TEST 1: Formal addressing (Sie)")
print("=" * 60)
customer_sie = customers[0]  # Hans Müller, Mann, sie
print(f"Customer: {customer_sie['vorname']} {customer_sie['nachname']}")
print(f"Gender: {customer_sie['gender']}, Du: {customer_sie['du']}")
msg = build_email(customer_sie, None, 'test@example.com')
for part in msg.walk():
    if part.get_content_type() == 'text/plain':
        body = part.get_payload(decode=True).decode('utf-8') if isinstance(part.get_payload(), str) and len(part.get_payload()) > 100 else part.get_payload()
        print(f"\nEmail body:\n{body}")
        print("\nExpected: 'Sehr geehrter Herr Müller' (formal)")
        nachname_check = 'Herr ' + customer_sie['nachname'] in body
        print(f"Contains 'Herr {customer_sie['nachname']}': {nachname_check}")
        print(f"Contains 'Ihre': {'Ihre' in body}")

# Test informal (du) addressing
print("\n" + "=" * 60)
print("TEST 2: Informal addressing (Du)")
print("=" * 60)
customer_du = customers[1]  # Anna Schmidt, Frau, du
print(f"Customer: {customer_du['vorname']} {customer_du['nachname']}")
print(f"Gender: {customer_du['gender']}, Du: {customer_du['du']}")
msg = build_email(customer_du, None, 'test@example.com')
for part in msg.walk():
    if part.get_content_type() == 'text/plain':
        body = part.get_payload(decode=True).decode('utf-8') if isinstance(part.get_payload(), str) and len(part.get_payload()) > 100 else part.get_payload()
        print(f"\nEmail body:\n{body}")
        print("\nExpected: 'Liebe Anna' (informal)")
        vorname_check = 'Liebe ' + customer_du['vorname'] in body
        print(f"Contains 'Liebe {customer_du['vorname']}': {vorname_check}")
        print(f"Contains 'deine': {'deine' in body}")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)

