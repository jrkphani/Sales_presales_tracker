"""
Validators Module
Provides validation utilities for data processing
"""

import re
from datetime import datetime

def validate_date_string(date_str):
    """
    Validate date string format
    
    Args:
        date_str (str): Date string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not date_str:
        return False
        
    try:
        datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return True
    except (ValueError, AttributeError):
        return False

def validate_email(email):
    """
    Validate email format
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not email:
        return False
        
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone):
    """
    Validate phone number format
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not phone:
        return False
        
    # Remove common separators and spaces
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check if remaining string is numeric and of reasonable length
    return cleaned.isdigit() and 8 <= len(cleaned) <= 15

def validate_amount(amount):
    """
    Validate monetary amount
    
    Args:
        amount: Amount to validate (string or number)
        
    Returns:
        bool: True if valid, False otherwise
    """
    if amount is None:
        return False
        
    try:
        float_amount = float(amount)
        return float_amount >= 0
    except (ValueError, TypeError):
        return False

def validate_percentage(value):
    """
    Validate percentage value
    
    Args:
        value: Percentage to validate (string or number)
        
    Returns:
        bool: True if valid, False otherwise
    """
    if value is None:
        return False
        
    try:
        float_value = float(value)
        return 0 <= float_value <= 100
    except (ValueError, TypeError):
        return False 