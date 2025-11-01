"""
SMTP configuration module.
Modify this module to switch between different email providers.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_smtp_config():
    """
    Get SMTP configuration settings.
    
    Modify this function to switch between Gmail, Outlook, or custom SMTP.
    
    Returns:
        Dictionary with SMTP settings:
        {
            'host': SMTP server hostname,
            'port': SMTP port (usually 587 for TLS),
            'username': Your email address,
            'password': Your email password or app password
        }
    """
    # Example: Gmail configuration
    # To use Gmail, you'll need an App Password:
    # https://support.google.com/accounts/answer/185833
    
    smtp_config = {
        'host': 'smtp.gmail.com',
        'port': 587,
        'username': os.getenv('EMAIL_USERNAME', 'raphaelbennohof@gmail.com'),
        'password': os.getenv('EMAIL_PASSWORD', 'your_app_password')
    }
    
    # Alternative: Outlook/Office365 configuration
    # Uncomment and modify if needed:
    # smtp_config = {
    #     'host': 'smtp.office365.com',
    #     'port': 587,
    #     'username': os.getenv('EMAIL_USERNAME', 'your_email@outlook.com'),
    #     'password': os.getenv('EMAIL_PASSWORD', 'your_password')
    # }
    
    # Alternative: Custom SMTP server
    # Uncomment and modify if needed:
    # smtp_config = {
    #     'host': 'smtp.yourcompany.com',
    #     'port': 587,
    #     'username': os.getenv('EMAIL_USERNAME', 'your_email@company.com'),
    #     'password': os.getenv('EMAIL_PASSWORD', 'your_password')
    # }
    
    return smtp_config

