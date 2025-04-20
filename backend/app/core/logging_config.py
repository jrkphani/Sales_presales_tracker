"""
Logging configuration module for the application.
Sets up logging with different handlers for different log levels.
"""

import os
import logging
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
logs_dir = Path('logs')
logs_dir.mkdir(exist_ok=True)

# Create a timestamp for the log file
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = logs_dir / f'zoho_fetch_{timestamp}.log'

# Configure logging
def setup_logger(name):
    """
    Set up a logger with file and console handlers.
    
    Args:
        name (str): Name of the logger
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 