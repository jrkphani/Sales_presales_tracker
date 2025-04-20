"""
Deal Data Model
Represents a Deal in the system
"""

from datetime import datetime

class Deal:
    """Deal model representing a sales opportunity"""
    
    def __init__(self, data):
        """
        Initialize a Deal from Zoho CRM data
        
        Args:
            data (dict): Raw deal data from Zoho CRM
        """
        self.id = data.get('id')
        self.name = data.get('Deal_Name')
        self.amount = float(data.get('Amount', 0))
        self.stage = data.get('Stage')
        self.probability = float(data.get('Probability', 0))
        self.closing_date = self._parse_date(data.get('Closing_Date'))
        self.account_name = data.get('Account_Name')
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
        """Convert Deal to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
            'stage': self.stage,
            'probability': self.probability,
            'closing_date': self.closing_date.isoformat() if self.closing_date else None,
            'account_name': self.account_name,
            'owner': self.owner,
            'created_time': self.created_time.isoformat() if self.created_time else None,
            'modified_time': self.modified_time.isoformat() if self.modified_time else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Deal instance from dictionary"""
        return cls(data)
    
    def __repr__(self):
        return f"<Deal {self.name} ({self.id})>" 