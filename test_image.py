"""Test image attachment"""
from email_builder import build_email
from config import IMAGE_FILE_PATH
import os

print(f"Testing image attachment...")
print(f"Image file: {IMAGE_FILE_PATH}")
print(f"File exists: {os.path.exists(IMAGE_FILE_PATH)}")

if os.path.exists(IMAGE_FILE_PATH):
    file_size = os.path.getsize(IMAGE_FILE_PATH)
    print(f"File size: {file_size} bytes ({file_size/1024:.2f} KB)")
    
    # Test building email with image
    customer = {
        'email': 'test@example.com',
        'name': 'Testuser',
        'gender': 'Mann'
    }
    
    msg = build_email(customer, IMAGE_FILE_PATH, 'test@example.com')
    
    # Check if image is attached
    has_image = False
    for part in msg.walk():
        if part.get_content_type().startswith('image/'):
            has_image = True
            print(f"\n[PASS] Image attached: {part.get_content_type()}")
            print(f"  Filename: {part.get_filename()}")
            break
    
    if not has_image:
        print("\n[FAIL] No image found in email")
else:
    print("\n[FAIL] Image file not found!")

