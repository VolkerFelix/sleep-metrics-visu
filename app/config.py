"""
Configuration settings for the Sleep Data Visualization application.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class."""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Sleep Data Microservice API configuration
    SLEEP_API_BASE_URL = os.environ.get(
        'SLEEP_API_BASE_URL', 
        'http://localhost:8001/api'
    )
    SLEEP_API_TIMEOUT = int(os.environ.get('SLEEP_API_TIMEOUT', 10))
    
    # Application settings
    ITEMS_PER_PAGE = int(os.environ.get('ITEMS_PER_PAGE', 10))
    DEFAULT_DATE_RANGE_DAYS = int(os.environ.get('DEFAULT_DATE_RANGE_DAYS', 7))