"""
Data Service Module
Handles data fetching and processing from Zoho CRM
"""

import logging
import json
import os
from datetime import datetime, timedelta
from flask import current_app
from app.core.zoho.bulk_reader import BulkReader
from app.core.zoho.transformers import DataTransformer
from app.models.deal import Deal
from app.models.account import Account

logger = logging.getLogger(__name__)

class DataService:
    """Service for fetching and processing Zoho CRM data"""
    
    def __init__(self, zoho_client, bulk_reader):
        """Initialize the service
        
        Args:
            zoho_client (ZohoClient): Client for direct Zoho CRM API calls
            bulk_reader (BulkReader): Client for bulk data operations
        """
        self.zoho_client = zoho_client
        self.bulk_reader = bulk_reader
        self.logger = logging.getLogger(__name__)
        self.transformer = DataTransformer()
    
    def fetch_all_data(self):
        """Fetch and transform all required data from Zoho CRM
        
        Returns:
            dict: Combined dashboard data with deals and accounts info
        """
        try:
            # Get currency info first
            currency_info = self.zoho_client.get_base_currency()
            
            # Get deals data
            deals_fields = self._get_module_fields('Deals')
            deals_data = self.bulk_reader.read_records('Deals', fields=deals_fields)
            transformed_deals = DataTransformer.transform_deals(deals_data, currency_info)
            
            # Get accounts data
            accounts_fields = self._get_module_fields('Accounts')
            accounts_data = self.bulk_reader.read_records('Accounts', fields=accounts_fields)
            transformed_accounts = DataTransformer.transform_accounts(accounts_data)
            
            # Combine and save data
            dashboard_data = DataTransformer.combine_dashboard_data(
                transformed_deals,
                transformed_accounts,
                currency_info
            )
            
            # Save to configured path
            self._save_dashboard_data(dashboard_data)
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Error fetching data: {str(e)}")
            # Return empty data structure with default USD currency
            return DataTransformer.combine_dashboard_data(
                DataTransformer.transform_deals([]),
                DataTransformer.transform_accounts([])
            )
    
    def _get_module_fields(self, module):
        """
        Dynamically fetch fields for a module from Zoho CRM
        
        Args:
            module (str): Module name (e.g., 'Deals', 'Accounts')
            
        Returns:
            list: List of field names to fetch
        """
        try:
            # Get field metadata from Zoho
            response = self.bulk_reader.client.get_module_fields(module)
            
            # Extract field names from response
            fields = []
            for field in response.get('fields', []):
                # Skip system fields and read-only fields if needed
                if field.get('system_field') or field.get('read_only'):
                    continue
                fields.append(field['api_name'])
                
            logger.info(f'Fetched {len(fields)} fields for {module}')
            return fields
            
        except Exception as e:
            logger.error(f'Failed to fetch fields for {module}: {str(e)}')
            # Fall back to essential fields if API call fails
            return self._get_essential_fields(module)
    
    def _get_essential_fields(self, module):
        """
        Fallback method to get essential fields for a module
        
        Args:
            module (str): Module name
            
        Returns:
            list: List of essential field names
        """
        essential_fields = {
            'Deals': [
                'Deal_Name',
                'Amount',
                'Stage',
                'Probability',
                'Closing_Date',
                'Account_Name',
                'Owner',
                'Created_Time',
                'Modified_Time'
            ],
            'Accounts': [
                'Account_Name',
                'Industry',
                'Account_Type',
                'Website',
                'Phone',
                'Billing_Country',
                'Billing_State',
                'Owner',
                'Created_Time',
                'Modified_Time'
            ]
        }
        logger.warning(f'Using essential fields for {module} due to API failure')
        return essential_fields.get(module, [])
    
    def _save_current_data(self, data):
        """Save current data to file"""
        data_path = current_app.config['DATA']['current_data_path']
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        
        with open(data_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _archive_old_data(self):
        """Archive current data with timestamp"""
        current_data_path = current_app.config['DATA']['current_data_path']
        archive_dir = current_app.config['DATA']['archive_dir']
        
        if not os.path.exists(current_data_path):
            return
            
        # Create archive directory if it doesn't exist
        os.makedirs(archive_dir, exist_ok=True)
        
        # Generate archive filename with timestamp
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        archive_path = os.path.join(archive_dir, f'data_{timestamp}.json')
        
        # Copy current data to archive
        with open(current_data_path, 'r') as src, open(archive_path, 'w') as dst:
            json.dump(json.load(src), dst, indent=2)
            
        # Clean up old archives
        self._cleanup_old_archives()
    
    def _cleanup_old_archives(self):
        """Remove archives older than retention period"""
        archive_dir = current_app.config['DATA']['archive_dir']
        retention_days = current_app.config['DATA']['archive_retention_days']
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        
        for filename in os.listdir(archive_dir):
            if not filename.startswith('data_') or not filename.endswith('.json'):
                continue
                
            filepath = os.path.join(archive_dir, filename)
            file_date = datetime.strptime(filename[5:19], '%Y%m%d_%H%M%S')
            
            if file_date < cutoff_date:
                os.remove(filepath)
                logger.info(f'Removed old archive: {filename}')

def trigger_data_refresh():
    """Trigger a manual data refresh"""
    service = DataService()
    return service.fetch_all_data() 