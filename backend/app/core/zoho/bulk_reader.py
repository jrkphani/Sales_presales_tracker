"""
Zoho Bulk Read Module
Handles bulk data reading operations from Zoho CRM using the official SDK v8
"""

import logging
import time
import os
import zipfile
import io
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from flask import current_app
from .client import ZohoClient

# Set up logging
logger = logging.getLogger(__name__)

class BulkReader:
    """Handles bulk reading of data from Zoho CRM using the official SDK v8"""
    
    def __init__(self, use_indian_dc: bool = True):
        """
        Initialize the BulkReader
        
        Args:
            use_indian_dc (bool): Whether to use Indian datacenter (default: True)
        """
        self.client = ZohoClient(use_indian_dc=use_indian_dc)
        self.data_dir = Path(current_app.config.get('ZOHO_DATA_DIR', 'backend/data'))
        self.data_dir.mkdir(exist_ok=True, parents=True)
    
    def submit_bulk_read_job(self, module: str, fields: List[str], criteria: Optional[str] = None) -> str:
        """
        Submit a bulk read job to Zoho CRM
        
        Args:
            module (str): Module name (e.g., 'Deals')
            fields (list): List of field names to fetch
            criteria (str, optional): Search criteria
            
        Returns:
            str: Job ID
            
        Raises:
            Exception: If job submission fails
        """
        try:
            return self.client.submit_bulk_read_job(module, fields, criteria)
        except Exception as e:
            logger.error(f"Failed to submit bulk read job for {module}: {str(e)}")
            raise
    
    def get_job_status(self, job_id: str) -> str:
        """
        Get the status of a bulk read job
        
        Args:
            job_id (str): Job ID to check
            
        Returns:
            str: Job status
            
        Raises:
            Exception: If status check fails
        """
        try:
            return self.client.get_bulk_read_job_status(job_id)
        except Exception as e:
            logger.error(f"Failed to get job status for {job_id}: {str(e)}")
            raise
    
    def download_results(self, job_id: str) -> Dict[str, Any]:
        """
        Download the results of a completed bulk read job
        
        Args:
            job_id (str): Job ID
            
        Returns:
            Dict containing:
                - 'file_path': Path to the downloaded CSV file
                - 'record_count': Number of records in the file
                - 'fields': List of fields in the file
            
        Raises:
            Exception: If download fails
        """
        try:
            # Get the file stream from the client
            response = self.client.download_bulk_read_results(job_id)
            
            # Create a timestamp for the file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Save the ZIP file
            zip_path = self.data_dir / f'bulk_read_{job_id}_{timestamp}.zip'
            with open(zip_path, 'wb') as f:
                f.write(response)
            
            # Extract the CSV file
            with zipfile.ZipFile(io.BytesIO(response)) as zip_ref:
                # Get the first CSV file
                csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
                if not csv_files:
                    raise ValueError("No CSV file found in ZIP archive")
                
                csv_filename = csv_files[0]
                csv_path = self.data_dir / f'bulk_read_{job_id}_{timestamp}.csv'
                
                # Extract the CSV file
                with zip_ref.open(csv_filename) as source, open(csv_path, 'wb') as target:
                    target.write(source.read())
            
            # Get record count and fields
            import pandas as pd
            df = pd.read_csv(csv_path)
            
            return {
                'file_path': str(csv_path),
                'record_count': len(df),
                'fields': list(df.columns)
            }
            
        except Exception as e:
            logger.error(f"Failed to download results for job {job_id}: {str(e)}")
            raise
    
    def wait_for_job_completion(self, job_id: str, timeout: int = 300, interval: int = 5) -> str:
        """
        Wait for a bulk read job to complete
        
        Args:
            job_id (str): Job ID
            timeout (int): Maximum time to wait in seconds
            interval (int): Time between status checks in seconds
            
        Returns:
            str: Final job status
            
        Raises:
            Exception: If job fails or times out
        """
        start_time = time.time()
        while True:
            status = self.get_job_status(job_id)
            
            if status == 'COMPLETED':
                return status
            elif status == 'FAILED':
                raise Exception(f'Bulk read job {job_id} failed')
            
            if time.time() - start_time > timeout:
                raise Exception(f'Timeout waiting for job {job_id}')
            
            time.sleep(interval)
    
    def get_module_fields(self, module: str) -> List[str]:
        """
        Get available fields for a module
        
        Args:
            module (str): Module name
            
        Returns:
            List[str]: List of available field names
            
        Raises:
            Exception: If field retrieval fails
        """
        try:
            return self.client.get_module_fields(module)
        except Exception as e:
            logger.error(f"Failed to get fields for module {module}: {str(e)}")
            raise
    
    def bulk_read_module(self, module: str, fields: Optional[List[str]] = None, 
                        criteria: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform a complete bulk read operation for a module
        
        Args:
            module (str): Module name
            fields (list, optional): List of fields to fetch. If None, all fields will be fetched
            criteria (str, optional): Search criteria
            
        Returns:
            Dict containing:
                - 'job_id': ID of the bulk read job
                - 'file_path': Path to the downloaded CSV file
                - 'record_count': Number of records in the file
                - 'fields': List of fields in the file
            
        Raises:
            Exception: If bulk read operation fails
        """
        try:
            # Get all available fields if none specified
            if fields is None:
                fields = self.get_module_fields(module)
            
            # Submit the job
            job_id = self.submit_bulk_read_job(module, fields, criteria)
            logger.info(f"Submitted bulk read job {job_id} for {module}")
            
            # Wait for completion
            status = self.wait_for_job_completion(job_id)
            logger.info(f"Job {job_id} completed with status: {status}")
            
            if status == 'COMPLETED':
                # Download and return results
                results = self.download_results(job_id)
                logger.info(f"Downloaded {results['record_count']} records for {module}")
                return {
                    'job_id': job_id,
                    **results
                }
            else:
                raise Exception(f'Job completed with unexpected status: {status}')
                
        except Exception as e:
            logger.error(f'Bulk read operation failed for {module}: {str(e)}')
            raise 