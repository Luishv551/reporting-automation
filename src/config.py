"""Configuration management."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration from environment variables."""

    # SMTP Configuration
    SMTP_HOST = os.getenv('SMTP_HOST', 'smtp-mail.outlook.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER = os.getenv('SMTP_USER', '')
    SMTP_PASS = os.getenv('SMTP_PASS', '')

    # Email Configuration
    EMAIL_FROM = os.getenv('EMAIL_FROM', SMTP_USER)
    EMAIL_TO = os.getenv('EMAIL_TO', '')

    # API Configuration
    API_HOST = os.getenv('API_HOST', '127.0.0.1')
    API_PORT = int(os.getenv('API_PORT', '8000'))


config = Config()
