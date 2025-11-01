"""
Central configuration for AutoMail script.
Modify these settings to match your CSV structure and requirements.
"""

# File paths
CSV_FILE_PATH = 'customers.csv'  # Path to your CSV file
IMAGE_FILE_PATH = 'Screenshot 2023-05-18 223048.png'    # Path to image to attach

# Rate limiting
EMAILS_PER_HOUR = 100
DELAY_SECONDS = 3600 / EMAILS_PER_HOUR  # 36 seconds per email

# CSV column mapping
# Change these to match your CSV column names
COLUMN_MAP = {
    'email': 'email',        # Column name in CSV for email address
    'vorname': 'vorname',    # Column name in CSV for first name
    'nachname': 'nachname',  # Column name in CSV for last name
    'anrede': 'anrede',      # Column name in CSV for salutation (Herr/Frau)
    'du': 'du'              # Column name in CSV for formality (sie/du)
}

