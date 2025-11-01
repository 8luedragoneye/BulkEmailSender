"""
Email building module for creating personalized email messages.
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os


def build_email(customer, image_path, sender_email):
    """
    Build a personalized email message with image attachment.
    
    Args:
        customer: Dictionary with customer data (email, name, gender)
        image_path: Path to image file to attach
        sender_email: Email address of sender
    
    Returns:
        MIMEMultipart email message object ready to send
    """
    # Create message container
    msg = MIMEMultipart('related')
    msg['From'] = sender_email
    msg['To'] = customer['email']
    msg['Subject'] = 'Ihre persönliche Nachricht'
    
    # Get customer name, default to "Kunde" if not available
    customer_name = customer.get('name', 'Kunde')
    customer_gender = customer.get('gender', '').strip()
    
    # Determine German salutation (Anrede) based on gender
    if customer_gender.lower() == 'mann':
        anrede = f"Sehr geehrter Herr {customer_name}"
    elif customer_gender.lower() == 'frau':
        anrede = f"Sehr geehrte Frau {customer_name}"
    else:
        # Generic greeting if gender is empty or unknown
        anrede = f"Guten Tag {customer_name}"
    
    # Create email body in German
    # Customize this template as needed
    body_text = f"""
{anrede},

dies ist Ihre persönliche E-Mail-Nachricht.

Mit freundlichen Grüßen,
AutoMail System
"""
    
    # Build HTML body with inline image
    # Check if image exists to include it inline
    image_cid = None
    if image_path and os.path.exists(image_path):
        image_cid = 'inline_image'
        body_html = f"""
<html>
  <head></head>
  <body>
    <p>{anrede},</p>
    <p>dies ist Ihre persönliche E-Mail-Nachricht.</p>
    <p><img src="cid:{image_cid}" alt="Image" style="max-width: 100%; height: auto;" /></p>
    <p>Mit freundlichen Grüßen,<br>AutoMail System</p>
  </body>
</html>
"""
    else:
        # HTML without image if image doesn't exist
        body_html = f"""
<html>
  <head></head>
  <body>
    <p>{anrede},</p>
    <p>dies ist Ihre persönliche E-Mail-Nachricht.</p>
    <p>Mit freundlichen Grüßen,<br>AutoMail System</p>
  </body>
</html>
"""
    
    # Attach text and HTML versions
    msg_text = MIMEText(body_text, 'plain')
    msg_html = MIMEText(body_html, 'html')
    
    # Create alternative part for multipart
    msg_alternative = MIMEMultipart('alternative')
    msg_alternative.attach(msg_text)
    msg_alternative.attach(msg_html)
    msg.attach(msg_alternative)
    
    # Embed image inline if file exists
    if image_path and os.path.exists(image_path):
        try:
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
            
            image = MIMEImage(img_data)
            image.add_header('Content-ID', f'<{image_cid}>')
            image.add_header('Content-Disposition', 'inline', filename=os.path.basename(image_path))
            msg.attach(image)
        except Exception as e:
            print(f"Warning: Could not embed image {image_path}: {e}")
    
    return msg

