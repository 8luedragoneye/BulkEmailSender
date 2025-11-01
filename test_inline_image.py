"""Test inline image embedding"""
from email_builder import build_email
from config import IMAGE_FILE_PATH
import os

print("Testing inline image embedding...")
print(f"Image file: {IMAGE_FILE_PATH}")

customer = {
    'email': 'test@example.com',
    'name': 'Testuser',
    'gender': 'Mann'
}

msg = build_email(customer, IMAGE_FILE_PATH, 'test@example.com')

# Check if image is embedded inline (Content-ID) vs attachment
has_inline = False
has_attachment = False

for part in msg.walk():
    content_disposition = str(part.get('Content-Disposition', ''))
    content_id = str(part.get('Content-ID', ''))
    
    if part.get_content_type().startswith('image/'):
        if 'inline' in content_disposition.lower():
            has_inline = True
            print(f"\n[PASS] Image embedded inline")
            print(f"  Content-ID: {content_id}")
            print(f"  Content-Disposition: {content_disposition}")
        elif 'attachment' in content_disposition.lower():
            has_attachment = True
            print(f"\n[WARNING] Image is attached, not inline")

# Check HTML for CID reference
html_content = None
for part in msg.walk():
    if part.get_content_type() == 'text/html':
        html_content = part.get_payload(decode=True).decode('utf-8')
        if 'cid:inline_image' in html_content:
            print(f"[PASS] HTML contains CID reference to image")
        break

if has_inline and 'cid:inline_image' in html_content:
    print("\n[SUCCESS] Image will be displayed inline in email!")
else:
    print("\n[FAIL] Image embedding check failed")

