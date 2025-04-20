"""
Helpers Module
Provides utility functions for the application
"""

import os
import json
from datetime import datetime
import psutil

def get_service_health():
    """
    Get service health information
    
    Returns:
        dict: Health check data
    """
    process = psutil.Process(os.getpid())
    
    return {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'memory_usage': {
            'rss': process.memory_info().rss / 1024 / 1024,  # MB
            'vms': process.memory_info().vms / 1024 / 1024   # MB
        },
        'cpu_percent': process.cpu_percent(),
        'uptime': process.create_time()
    }

def safe_json_loads(json_str, default=None):
    """
    Safely load JSON string
    
    Args:
        json_str (str): JSON string to parse
        default: Default value if parsing fails
        
    Returns:
        Parsed JSON data or default value
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default

def format_currency(amount, currency='USD'):
    """
    Format currency amount
    
    Args:
        amount (float): Amount to format
        currency (str): Currency code
        
    Returns:
        str: Formatted currency string
    """
    try:
        return f'{currency} {float(amount):,.2f}'
    except (ValueError, TypeError):
        return f'{currency} 0.00'

def format_percentage(value):
    """
    Format percentage value
    
    Args:
        value (float): Value to format
        
    Returns:
        str: Formatted percentage string
    """
    try:
        return f'{float(value):.1f}%'
    except (ValueError, TypeError):
        return '0.0%'

def safe_divide(numerator, denominator):
    """
    Safely divide two numbers
    
    Args:
        numerator: Number to divide
        denominator: Number to divide by
        
    Returns:
        float: Result of division or 0 if invalid
    """
    try:
        if denominator == 0:
            return 0
        return float(numerator) / float(denominator)
    except (ValueError, TypeError):
        return 0 