import os
SQLALCHEMY_DATABASE_URI = 'sqlite:///budgetnest.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Flask-WTF CSRF protection
# CSRF_ENABLED = True

# Use an environment variable if set, otherwise use this default (not for production)
SECRET_KEY = os.environ.get('SECRET_KEY', 'your_development_secret_key_here')
DEBUG = True
# config.py


# Flask settings
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'

# Flask-Mail settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'princesssopeju@gmail.com'
MAIL_PASSWORD = 'wmlh tcgl zwwf vnsj'  # Your app-specific password if 2FA is enabled
MAIL_DEFAULT_SENDER = 'princesssopeju@gmail.com'
