# AutoMail

A professional, modular email automation system for sending personalized bulk emails from CSV data with built-in rate limiting, German language support, and inline image embedding.

## Overview

AutoMail is a Python-based email automation tool designed to send personalized emails to large customer lists efficiently and safely. It features a modular architecture that allows independent configuration of CSV structure, SMTP settings, and email templates, making it easy to adapt to different requirements without modifying core functionality.

### Key Features

- **Cross-Platform**: Runs seamlessly on Windows, macOS, and Linux
- **Modular Architecture**: Separate modules for CSV parsing, SMTP configuration, email building, and sending logic
- **Intelligent Rate Limiting**: Configurable sending rate (default: 100 emails/hour) to prevent server overload
- **German Language Support**: Automatic gender-based salutation (Anrede) with support for "Mann", "Frau", or generic greetings
- **Inline Image Embedding**: Images displayed directly in email body, not as attachments
- **CSV Flexibility**: Configurable column mapping to adapt to any CSV structure
- **Multiple SMTP Providers**: Support for Gmail, Outlook/Office365, and custom SMTP servers
- **Error Handling**: Robust error handling with detailed logging and failure tracking

## Requirements

- Python 3.7 or higher
- Dependencies listed in `requirements.txt`

## Installation

1. **Clone or download the repository**

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your environment**:
   - Copy `.env` template (if provided) or create `.env` file with:
     ```
     EMAIL_USERNAME=your_email@gmail.com
     EMAIL_PASSWORD=your_app_password
     ```

## Quick Start

1. **Prepare your CSV file**:
   - Create a CSV file with columns: `email`, `name`, `gender`
   - Place it in the project directory or update the path in `config.py`
   - Example CSV structure:
     ```csv
     email,name,gender
     customer1@example.com,Max Mustermann,Mann
     customer2@example.com,Anna Schmidt,Frau
     ```

2. **Configure the application**:
   - Edit `config.py` to set:
     - `CSV_FILE_PATH`: Path to your customer CSV file
     - `IMAGE_FILE_PATH`: Path to image file for inline embedding (optional)
     - `COLUMN_MAP`: Map your CSV columns if they differ from standard names

3. **Set up email credentials**:
   - Option A: Create `.env` file with `EMAIL_USERNAME` and `EMAIL_PASSWORD`
   - Option B: Set environment variables
   - Option C: Edit `smtp_config.py` directly (not recommended for production)

4. **Run the application**:
   ```bash
   python main.py
   ```

5. **Confirm and monitor**:
   - Review the configuration summary
   - Confirm sending when prompted
   - Monitor progress as emails are sent

## Configuration

### CSV Column Mapping

If your CSV uses different column names, update `COLUMN_MAP` in `config.py`:

```python
COLUMN_MAP = {
    'email': 'Email',      # Your CSV column name for email
    'name': 'FullName',     # Your CSV column name for name
    'gender': 'Geschlecht'  # Your CSV column name for gender
}
```

### Email Service Configuration

#### Gmail Setup
1. Enable 2-Step Verification in your Google Account
2. Generate an App Password: https://support.google.com/accounts/answer/185833
3. Use the 16-character app password in `.env` file

#### Outlook/Office365 Setup
1. Update `smtp_config.py`:
   ```python
   smtp_config = {
       'host': 'smtp.office365.com',
       'port': 587,
       'username': os.getenv('EMAIL_USERNAME'),
       'password': os.getenv('EMAIL_PASSWORD')
   }
   ```

### Rate Limiting

Adjust sending rate in `config.py`:

```python
EMAILS_PER_HOUR = 100  # Change to your desired rate
```

Calculation: Delay between emails = 3600 / EMAILS_PER_HOUR seconds

## Project Structure

```
AutoMail/
├── main.py                 # Main entry point and orchestration
├── config.py               # Central configuration settings
├── csv_reader.py           # CSV parsing and column mapping
├── smtp_config.py          # SMTP server configuration
├── email_builder.py        # Email template and inline image embedding
├── sender.py               # Rate limiting and email sending logic
├── requirements.txt         # Python dependencies
├── .env                    # Environment variables (credentials)
├── .gitignore              # Git ignore rules
├── customers.csv           # Customer data file
└── README.md               # This file
```

## Email Features

### German Language Support

The system automatically generates appropriate German salutations based on gender:

- **"Mann"** → "Sehr geehrter Herr [Name]"
- **"Frau"** → "Sehr geehrte Frau [Name]"
- **Empty/Unknown** → "Guten Tag [Name]"

### Inline Images

Images are embedded directly in the email body using CID (Content-ID) references, ensuring they display inline rather than as attachments. The email structure is:

1. Anrede (Salutation)
2. Text (Message body)
3. Image (Inline embedded)
4. Grüße (Closing)

## Usage Examples

### Basic Usage
```bash
python main.py
```

### Testing CSV Reading
```bash
python test_main.py
```

### Testing Email Building
```bash
python test_german_email.py
```

## Email Template Customization

Edit `email_builder.py` to customize:

- Email subject
- Email body text
- HTML formatting
- Image placement and styling

Example modification:
```python
msg['Subject'] = 'Your Custom Subject'
body_html = f"""
<html>
  <body>
    <p>{anrede},</p>
    <p>Your custom message here.</p>
    <p><img src="cid:{image_cid}" style="max-width: 600px;" /></p>
    <p>Your closing message</p>
  </body>
</html>
"""
```

## Security Best Practices

1. **Never commit `.env` file**: It's automatically ignored by `.gitignore`
2. **Use App Passwords**: Never use your main email password
3. **Review CSV data**: Ensure customer email addresses are valid
4. **Test with small batches**: Test with a few emails before sending to large lists

## Troubleshooting

### Authentication Errors
- **Gmail**: Ensure 2-Step Verification is enabled and you're using an App Password
- **Outlook**: Verify credentials and ensure account allows SMTP access
- **Generic**: Check username/password in `.env` file

### CSV Reading Issues
- Verify CSV file path in `config.py`
- Check that `COLUMN_MAP` matches your CSV column names
- Ensure CSV has proper header row
- Validate email addresses are in correct format

### Image Not Displaying
- Verify image file path in `config.py`
- Check file exists and is readable
- Ensure image format is supported (PNG, JPG, GIF, BMP)
- Test with smaller image files if email size is an issue

### Rate Limiting Issues
- Adjust `EMAILS_PER_HOUR` in `config.py` if needed
- Some email providers have their own rate limits
- Monitor for any "too many requests" errors

## Support

For issues, questions, or contributions:

1. Review the troubleshooting section
2. Check configuration files for errors
3. Verify all dependencies are installed
4. Test with a single email first

## License

This project is provided as-is for email automation purposes.

## Version

Current Version: 1.0.0

---

**Important**: Always test with a small batch of emails before sending to your full customer list. Ensure compliance with email marketing regulations (GDPR, CAN-SPAM, etc.) in your jurisdiction.
