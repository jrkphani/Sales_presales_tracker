"""
Settings Module
Handles application configuration and environment variables
"""

import os
from dotenv import load_dotenv

def validate_config(config):
    """Validate required configuration settings"""
    # Validate Zoho API settings
    zoho_api = config.get('ZOHO_API', {})
    required_zoho_settings = ['client_id', 'client_secret', 'refresh_token']
    missing_settings = [setting for setting in required_zoho_settings if not zoho_api.get(setting)]
    
    if missing_settings:
        raise ValueError(f"Missing required Zoho API settings: {', '.join(missing_settings)}")
    
    # Validate data settings
    data_config = config.get('DATA', {})
    if not os.path.exists(os.path.dirname(data_config.get('current_data_path', ''))):
        os.makedirs(os.path.dirname(data_config.get('current_data_path', '')))
    
    if not os.path.exists(data_config.get('archive_dir', '')):
        os.makedirs(data_config.get('archive_dir', ''))

def load_config(app):
    """Load configuration into Flask application"""
    # Load environment variables from .env file
    load_dotenv()
    
    # Flask settings
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', '0') == '1'
    app.config['PORT'] = int(os.getenv('PORT', '5000'))
    
    # Zoho API settings
    app.config['ZOHO_API'] = {
        'client_id': os.getenv('ZOHO_CLIENT_ID'),
        'client_secret': os.getenv('ZOHO_CLIENT_SECRET'),
        'refresh_token': os.getenv('ZOHO_REFRESH_TOKEN'),
        'api_domain': os.getenv('ZOHO_API_DOMAIN', 'https://www.zohoapis.com'),
        'crm_domain': os.getenv('ZOHO_CRM_DOMAIN', 'https://www.zohoapis.in')
    }
    
    # Data settings
    app.config['DATA'] = {
        'refresh_interval': int(os.getenv('DATA_REFRESH_INTERVAL', '24')),
        'archive_retention_days': int(os.getenv('ARCHIVE_RETENTION_DAYS', '30')),
        'current_data_path': os.path.join('data', 'current-data.json'),
        'archive_dir': os.path.join('data', 'archive')
    }
    
    # Validate required configuration
    validate_config(app.config) 