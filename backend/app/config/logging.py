"""
Logging Configuration Module
Sets up application logging
"""

import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    """Configure logging for the application"""
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Set up file handler
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    
    # Set formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # Set log level based on debug mode
    if app.debug:
        file_handler.setLevel(logging.DEBUG)
    else:
        file_handler.setLevel(logging.INFO)
    
    # Add handler to app logger
    app.logger.addHandler(file_handler)
    
    # Configure logging for Zoho client
    zoho_logger = logging.getLogger('zoho')
    zoho_logger.setLevel(logging.INFO)
    zoho_logger.addHandler(file_handler)
    
    # Log application startup
    app.logger.info('Application logging configured') 