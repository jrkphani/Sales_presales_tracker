"""
Zoho API Client Module
Handles communication with Zoho CRM API using the official SDK
"""

import logging
from zohocrmsdk.src.com.zoho.crm.api.initializer import Initializer
from zohocrmsdk.src.com.zoho.crm.api.record import Record
from zohocrmsdk.src.com.zoho.crm.api.users import Users
from zohocrmsdk.src.com.zoho.crm.api.settings import Settings
from zohocrmsdk.src.com.zoho.crm.api.bulk_read import BulkRead
from zohocrmsdk.src.com.zoho.crm.api.currencies import CurrenciesOperations
from flask import current_app
from zohocrmsdk.src.com.zoho.crm.api.org import OrganizationOperations
from zohocrmsdk.src.com.zoho.crm.api.org import OrganizationOperations as ZOHOCRMSDK

logger = logging.getLogger(__name__)

class ZohoClient:
    """Client for interacting with Zoho CRM API"""
    
    def __init__(self, use_indian_dc=False):
        """Initialize the Zoho CRM client
        
        Args:
            use_indian_dc (bool): Whether to use Indian datacenter
        """
        self.use_indian_dc = use_indian_dc
        self.initialize_sdk()
    
    def initialize_sdk(self):
        """Initialize the Zoho CRM SDK"""
        try:
            Initializer.initialize()
            self.zoho_crm = Initializer.get_api_client()
        except Exception as e:
            logger.error(f'Failed to initialize SDK: {str(e)}')
            raise
    
    def _get_module_instance(self, module_name):
        """
        Get a module instance from the SDK
        
        Args:
            module_name (str): Name of the module
            
        Returns:
            Module instance
        """
        try:
            return Record(module_name)
        except Exception as e:
            logger.error(f'Failed to get module instance for {module_name}: {str(e)}')
            raise
    
    def get_module_fields(self, module):
        """Get field metadata for a module"""
        try:
            settings = Settings()
            return settings.get_fields(module)
        except Exception as e:
            logger.error(f'Failed to get fields for {module}: {str(e)}')
            raise
    
    def get_records(self, module, fields=None, criteria=None, page=1):
        """Get records from a module with pagination"""
        try:
            module_instance = self._get_module_instance(module)
            
            # Prepare parameters
            param_instance = module_instance.get_param_instance()
            if fields:
                param_instance.add_key('fields', ','.join(fields))
            if criteria:
                param_instance.add_key('criteria', criteria)
            param_instance.add_key('page', page)
            param_instance.add_key('per_page', 200)
            
            # Get records
            return module_instance.get_records(param_instance)
            
        except Exception as e:
            logger.error(f'Failed to get records for {module}: {str(e)}')
            raise
    
    def get_users(self):
        """Get all users from Zoho CRM"""
        try:
            users = Users()
            param_instance = users.get_param_instance()
            param_instance.add_key('type', 'AllUsers')
            return users.get_users(param_instance)
        except Exception as e:
            logger.error(f'Failed to get users: {str(e)}')
            raise
    
    def get_base_currency(self):
        """Get the organization's base currency information
        
        Returns:
            dict: Currency information with code, symbol and name
                 e.g. {'code': 'USD', 'symbol': '$', 'name': 'US Dollar'}
                 Returns None if currency info cannot be fetched
        """
        try:
            # Get org info which includes currency
            org_ops = ZOHOCRMSDK.Org.OrganizationOperations()
            response = org_ops.get_organization()
            
            if response.get_status_code() == 200:
                org = response.get_response_object()[0]
                currency = org.get_currency_symbol()
                if currency:
                    return {
                        'code': currency.get_currency_code(),
                        'symbol': currency.get_symbol(),
                        'name': currency.get_currency_name()
                    }
            
            logger.warning("Could not fetch currency info, using USD as default")
            return {
                'code': 'USD',
                'symbol': '$',
                'name': 'US Dollar'
            }
            
        except Exception as e:
            logger.error(f"Error getting currency info: {str(e)}")
            # Return USD as default
            return {
                'code': 'USD',
                'symbol': '$',
                'name': 'US Dollar'
            }
    
    def submit_bulk_read_job(self, module, fields, criteria=None):
        """
        Submit a bulk read job
        
        Args:
            module (str): Module name
            fields (list): List of fields to fetch
            criteria (str): Search criteria
            
        Returns:
            str: Job ID
        """
        try:
            bulk_read = BulkRead()
            
            # Prepare request body
            request_body = {
                'callback': {
                    'url': '',
                    'method': 'post'
                },
                'query': {
                    'module': module,
                    'fields': fields
                }
            }
            
            if criteria:
                request_body['query']['criteria'] = criteria
            
            # Submit job
            response = bulk_read.create_bulk_read_job(request_body)
            job_id = response.get_data()[0].get_details().get('id')
            
            logger.info(f'Submitted bulk read job for {module}. Job ID: {job_id}')
            return job_id
            
        except Exception as e:
            logger.error(f'Failed to submit bulk read job for {module}: {str(e)}')
            raise
    
    def get_bulk_read_job_status(self, job_id):
        """Get the status of a bulk read job"""
        try:
            bulk_read = BulkRead()
            response = bulk_read.get_bulk_read_job(job_id)
            return response.get_data()[0].get_state()
        except Exception as e:
            logger.error(f'Failed to get bulk read job status for {job_id}: {str(e)}')
            raise
    
    def download_bulk_read_results(self, job_id):
        """Download the results of a completed bulk read job"""
        try:
            bulk_read = BulkRead()
            response = bulk_read.download_bulk_read_result(job_id)
            return response.get_data()
        except Exception as e:
            logger.error(f'Failed to download bulk read results for {job_id}: {str(e)}')
            raise