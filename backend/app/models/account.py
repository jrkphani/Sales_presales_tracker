"""
Account Data Model
Represents an Account in the system
"""

from datetime import datetime

class Account:
    """Account model representing a customer account"""
    
    def __init__(self, data):
        """
        Initialize an Account from Zoho CRM data
        
        Args:
            data (dict): Raw account data from Zoho CRM
        """
        self.id = data.get('id')
        self.name = data.get('Account_Name')
        self.industry = data.get('Industry')
        self.type = data.get('Account_Type')
        self.website = data.get('Website')
        self.phone = data.get('Phone')
        self.billing_country = data.get('Billing_Country')
        self.billing_state = data.get('Billing_State')
        self.owner = data.get('Owner')
        self.created_time = self._parse_date(data.get('Created_Time'))
        self.modified_time = self._parse_date(data.get('Modified_Time'))
    
    def _parse_date(self, date_str):
        """Parse date string to datetime object"""
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None
    
    def to_dict(self):
        """Convert Account to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'industry': self.industry,
            'type': self.type,
            'website': self.website,
            'phone': self.phone,
            'billing_country': self.billing_country,
            'billing_state': self.billing_state,
            'owner': self.owner,
            'created_time': self.created_time.isoformat() if self.created_time else None,
            'modified_time': self.modified_time.isoformat() if self.modified_time else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Account instance from dictionary"""
        return cls(data)
    
    def __repr__(self):
        return f"<Account {self.name} ({self.id})>" 