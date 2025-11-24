"""Configuration management."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration from environment variables."""

    # Email Configuration (uses Outlook COM API)
    EMAIL_TO = os.getenv('EMAIL_TO', '')

    # API Configuration
    API_HOST = os.getenv('API_HOST', '127.0.0.1')
    API_PORT = int(os.getenv('API_PORT', '8000'))


config = Config()
