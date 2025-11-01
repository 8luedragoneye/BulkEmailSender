"""Test .env file loading"""
from smtp_config import get_smtp_config

config = get_smtp_config()
print('SMTP Config loaded:')
print(f'  Username: {config["username"]}')
if config['password'] == 'your_app_password_here':
    print('  Password: [NOT SET - please update .env file with your app password]')
else:
    print('  Password: *** (loaded from .env)')

