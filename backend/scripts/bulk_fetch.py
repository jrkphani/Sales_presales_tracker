"""
Bulk Fetch Script
Triggers bulk fetch operations from Zoho CRM using the BulkReader class
"""

import os
import sys
import json
import time
import logging
import base64
import io
import zipfile
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Any

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from zohocrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken
from zohocrmsdk.src.com.zoho.crm.api.dc import INDataCenter
from zohocrmsdk.src.com.zoho.crm.api.initializer import Initializer
from zohocrmsdk.src.com.zoho.api.authenticator.store.file_store import FileStore
from zohocrmsdk.src.com.zoho.crm.api.sdk_config import SDKConfig
from zohocrmsdk.src.com.zoho.api.logger import Logger
from zohocrmsdk.src.com.zoho.crm.api.bulk_read import APIException, BulkReadOperations, ResponseWrapper, BodyWrapper, CallBack, Query, Criteria, ActionWrapper
from zohocrmsdk.src.com.zoho.crm.api.util.choice import Choice
from zohocrmsdk.src.com.zoho.crm.api.modules import MinifiedModule
from zohocrmsdk.src.com.zoho.crm.api.bulk_read.action_handler import ActionHandler
from zohocrmsdk.src.com.zoho.crm.api.bulk_read.response_handler import ResponseHandler
from zohocrmsdk.src.com.zoho.crm.api.fields import FieldsOperations, ResponseHandler as FieldsResponseHandler
from zohocrmsdk.src.com.zoho.crm.api.fields import ParameterMap

# Set up logging
def setup_logger(name):
    """Set up a logger with file and console handlers"""
    # Create logs directory if it doesn't exist
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    
    # Create a timestamp for the log file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = logs_dir / f'zoho_fetch_{timestamp}.log'
    
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

# Set up logger
logger = setup_logger('zoho_bulk_fetch')

def initialize_sdk():
    """Initialize the Zoho CRM SDK"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Create OAuth token
        token = OAuthToken(
            client_id=os.getenv('ZOHO_CLIENT_ID'),
            client_secret=os.getenv('ZOHO_CLIENT_SECRET'),
            refresh_token=os.getenv('ZOHO_REFRESH_TOKEN')
        )
        
        # Initialize the SDK
        Initializer.initialize(
            environment=INDataCenter.PRODUCTION(),
            token=token,
            sdk_config=SDKConfig(auto_refresh_fields=True, pick_list_validation=False)
        )
        
        logger.info('Zoho CRM SDK initialized successfully')
        
    except Exception as e:
        logger.error(f'Failed to initialize Zoho CRM SDK: {str(e)}', exc_info=True)
        raise

def submit_bulk_read_job(module: str, fields: List[str]) -> str:
    """
    Submit a bulk read job for the specified module and fields.
    
    Args:
        module: The module name (e.g., 'Leads', 'Contacts')
        fields: List of fields to fetch
        
    Returns:
        str: The job ID if successful
        
    Raises:
        Exception: If job submission fails
    """
    try:
        # Initialize bulk read operations
        bulk_read_operations = BulkReadOperations()
        
        # Create request body wrapper
        request = BodyWrapper()
        
        # Create module instance
        module_instance = MinifiedModule()
        module_instance.set_api_name(module)
        
        # Set query details
        query = Query()
        query.set_module(module_instance)
        query.set_fields(fields)
        query.set_page(1)
        request.set_query(query)
        
        # Submit the bulk read job
        response = bulk_read_operations.create_bulk_read_job(request)
        
        # Log response status
        logger.info(f"Response status code: {response.get_status_code()}")
        
        if response.get_status_code() in [200, 201, 202]:
            # Handle different response types
            response_obj = response.get_object()
            if isinstance(response_obj, ActionHandler):
                data = response_obj.get_data()
                job_id = data[0].get_details().get('id')
                logger.info(f"Successfully submitted bulk read job. Job ID: {job_id}")
                return job_id
            elif isinstance(response_obj, ResponseHandler):
                data = response_obj.get_data()
                job_id = data[0].get_details().get('id')
                logger.info(f"Successfully submitted bulk read job. Job ID: {job_id}")
                return job_id
            else:
                raise Exception(f"Unexpected response type: {type(response_obj)}")
        else:
            error_msg = response.get_object().get_message()
            raise Exception(f"Failed to submit bulk read job: {error_msg}")
            
    except Exception as e:
        logger.error(f"Failed to submit bulk read job for {module}: {str(e)}")
        raise

def get_job_status(job_id: str) -> str:
    """
    Get the status of a bulk read job.
    
    Args:
        job_id: The job ID to check
        
    Returns:
        str: The job status
        
    Raises:
        Exception: If job status check fails
    """
    try:
        # Convert job_id to integer since the SDK expects it
        job_id_int = int(job_id)
        bulk_read_operations = BulkReadOperations()
        response = bulk_read_operations.get_bulk_read_job_details(job_id_int)
        
        if response.get_status_code() in [200, 201, 202]:
            response_obj = response.get_object()
            if isinstance(response_obj, ResponseHandler):
                data = response_obj.get_data()
                if data:
                    return data[0].get_state().get_value()
            
        raise Exception(f"Failed to get job status: {response.get_object().get_message()}")
            
    except Exception as e:
        logger.error(f"Failed to get job status for {job_id}: {str(e)}")
        raise

def extract_csv_from_response(response_wrapper) -> bytes:
    """
    Extract data directly from the bulk read response.
    
    Args:
        response_wrapper: The FileBodyWrapper response from the bulk read operation
        
    Returns:
        bytes: The raw data from the response
    """
    try:
        # Get the stream from FileBodyWrapper
        stream_wrapper = response_wrapper.get_file()
        if not stream_wrapper:
            raise ValueError("No file stream found in response")
            
        # Get the response content
        response = stream_wrapper.get_stream()
        if not response:
            raise ValueError("No response stream available")
            
        # Try to get the raw content directly
        try:
            # First attempt: try to get raw content directly
            content = response.raw.read()
            if not content:
                raise ValueError("No content in response stream")
                
            # Check if the content is a ZIP file (starts with PK\x03\x04)
            if content.startswith(b'PK\x03\x04'):
                logger.info("Detected ZIP file in response")
                
                # Create data directory if it doesn't exist
                data_dir = Path('/Users/jrkphani/Projects/Sales_presales_tracker/backend/data')
                data_dir.mkdir(exist_ok=True, parents=True)
                
                # Save the ZIP file
                zip_file = data_dir / f'bulk_read_{int(time.time())}.zip'
                logger.info(f"Saving ZIP file to: {zip_file}")
                
                with open(zip_file, 'wb') as f:
                    f.write(content)
                    
                logger.info(f"Successfully downloaded and saved ZIP file to {zip_file}")
                
                # Extract the CSV file from the ZIP
                import zipfile
                import io
                
                with zipfile.ZipFile(io.BytesIO(content)) as zip_ref:
                    # List files in the ZIP
                    file_list = zip_ref.namelist()
                    logger.info(f"Files in ZIP: {file_list}")
                    
                    # Extract the first CSV file
                    csv_filename = next((f for f in file_list if f.endswith('.csv')), None)
                    if csv_filename:
                        logger.info(f"Extracting CSV file: {csv_filename}")
                        csv_data = zip_ref.read(csv_filename)
                        
                        # Save the CSV file
                        csv_file = data_dir / f'bulk_read_{int(time.time())}.csv'
                        logger.info(f"Saving CSV file to: {csv_file}")
                        
                        with open(csv_file, 'wb') as f:
                            f.write(csv_data)
                            
                        logger.info(f"Successfully extracted and saved CSV file to {csv_file}")
                        
                        # Verify the file was created
                        if csv_file.exists():
                            logger.info(f"CSV file exists and has size: {csv_file.stat().st_size} bytes")
                        else:
                            logger.error(f"CSV file was not created at {csv_file}")
                            
                        return csv_data
                    else:
                        logger.error("No CSV file found in ZIP")
                        return content
                        
            return content
                
        except Exception as e:
            logger.warning(f"Failed to read raw content: {str(e)}")
            # Second attempt: try to read the stream in chunks
            content = b""
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    content += chunk
                    
            if not content:
                raise ValueError("No content in response stream")
                
            return content
            
    except Exception as e:
        logger.error(f"Failed to extract data: {str(e)}")
        raise

def download_results(job_id: str) -> str:
    """
    Download the results of a completed bulk read job and save as a file.
    
    Args:
        job_id: The job ID to download results for
        
    Returns:
        str: The path to the downloaded file
    """
    try:
        # Convert job_id to integer since the SDK expects it
        job_id_int = int(job_id)
        bulk_read_operations = BulkReadOperations()
        
        # Get the download URL
        logger.info(f"Downloading results for job ID: {job_id}")
        response = bulk_read_operations.download_result(job_id_int)
        
        # Log response details for debugging
        logger.info(f"Download response status code: {response.get_status_code()}")
        
        if response.get_status_code() in [200, 201, 202]:
            # Get the response data
            response_wrapper = response.get_object()
            
            # Log response wrapper type for debugging
            logger.info(f"Response wrapper type: {type(response_wrapper)}")
            
            # Extract data
            data = extract_csv_from_response(response_wrapper)
            
            # Create data directory if it doesn't exist
            # Use absolute path
            data_dir = Path('/Users/jrkphani/Projects/Sales_presales_tracker/backend/data')
            data_dir.mkdir(exist_ok=True, parents=True)
            
            # Check if the data is a ZIP file
            if data.startswith(b'PK\x03\x04'):
                logger.info("Detected ZIP file in response")
                
                # Save ZIP file
                zip_file = data_dir / f'bulk_read_{job_id}.zip'
                logger.info(f"Saving ZIP file to: {zip_file}")
                
                with open(zip_file, 'wb') as f:
                    f.write(data)
                    
                logger.info(f"Successfully downloaded and saved ZIP file to {zip_file}")
                
                # Extract CSV from ZIP
                import zipfile
                import io
                
                with zipfile.ZipFile(io.BytesIO(data)) as zip_ref:
                    # List files in the ZIP
                    file_list = zip_ref.namelist()
                    logger.info(f"Files in ZIP: {file_list}")
                    
                    # Extract the first CSV file
                    csv_filename = next((f for f in file_list if f.endswith('.csv')), None)
                    if csv_filename:
                        logger.info(f"Extracting CSV file: {csv_filename}")
                        csv_data = zip_ref.read(csv_filename)
                        
                        # Save CSV file
                        csv_file = data_dir / f'bulk_read_{job_id}.csv'
                        logger.info(f"Saving CSV file to: {csv_file}")
                        
                        with open(csv_file, 'wb') as f:
                            f.write(csv_data)
                            
                        logger.info(f"Successfully extracted and saved CSV file to {csv_file}")
                        
                        # Verify file was created
                        if csv_file.exists():
                            logger.info(f"CSV file exists and has size: {csv_file.stat().st_size} bytes")
                        else:
                            logger.error(f"CSV file was not created at {csv_file}")
                            
                        return str(csv_file)
                    else:
                        logger.error("No CSV file found in ZIP")
                        return str(zip_file)
            else:
                # Save file with binary mode
                file_path = data_dir / f'bulk_read_{job_id}.csv'
                logger.info(f"Saving file to: {file_path}")
                
                with open(file_path, 'wb') as f:
                    f.write(data)
                    
                logger.info(f"Successfully downloaded and saved file to {file_path}")
                
                # Verify file was created
                if file_path.exists():
                    logger.info(f"File exists and has size: {file_path.stat().st_size} bytes")
                else:
                    logger.error(f"File was not created at {file_path}")
                    
                return str(file_path)
        else:
            error_msg = response.get_object().get_message()
            raise Exception(f"Failed to download results: {error_msg}")
            
    except Exception as e:
        logger.error(f"Failed to download results for job {job_id}: {str(e)}")
        raise

def wait_for_job_completion(job_id, timeout=300, interval=5):
    """Wait for a bulk read job to complete"""
    start_time = datetime.now()
    logger.info(f'Waiting for job {job_id} to complete (timeout: {timeout}s)')
    
    while True:
        status = get_job_status(job_id)
        
        if status == 'COMPLETED':
            logger.info(f'Job {job_id} completed successfully')
            return status
        elif status == 'FAILED':
            logger.error(f'Job {job_id} failed')
            raise Exception(f'Bulk read job {job_id} failed')
        
        if (datetime.now() - start_time).total_seconds() > timeout:
            logger.error(f'Timeout waiting for job {job_id}')
            raise Exception(f'Timeout waiting for job {job_id}')
        
        logger.info(f'Job status: {status}, waiting {interval} seconds...')
        time.sleep(interval)

def get_module_fields(module: str) -> List[str]:
    """
    Get all available fields (including custom fields) for a module.
    
    Args:
        module: The module name (e.g., 'Deals', 'Leads')
        
    Returns:
        List[str]: List of field API names
    """
    try:
        # Initialize fields operations
        fields_operations = FieldsOperations()
        
        # Create parameter map
        param_instance = ParameterMap()
        
        # Create module instance
        module_instance = MinifiedModule()
        module_instance.set_api_name(module)
        
        # Get fields for the module
        response = fields_operations.get_fields(module_instance, param_instance)
        
        if response.get_status_code() in [200, 201, 202]:
            response_obj = response.get_object()
            if isinstance(response_obj, FieldsResponseHandler):
                fields = response_obj.get_fields()
                # Extract field API names
                field_names = [field.get_api_name() for field in fields]
                logger.info(f"Found {len(field_names)} fields for {module}")
                logger.debug(f"Fields: {field_names}")
                return field_names
            else:
                raise Exception(f"Unexpected response type: {type(response_obj)}")
        else:
            error_msg = response.get_object().get_message()
            raise Exception(f"Failed to get fields: {error_msg}")
            
    except Exception as e:
        logger.error(f"Failed to get fields for {module}: {str(e)}")
        # Return default fields if we can't get the complete list
        if module == 'Deals':
            return ['id', 'Deal_Name', 'Account_Name', 'Stage', 'Amount', 'Closing_Date', 'Created_Time', 'Modified_Time',
                   'Owner', 'Description', 'Pipeline', 'Lead_Source', 'Contact_Name', 'Type', 'Next_Step', 'Expected_Revenue']
        elif module == 'Leads':
            return ['id', 'First_Name', 'Last_Name', 'Email', 'Phone', 'Company', 'Lead_Status', 'Created_Time', 'Modified_Time']
        elif module == 'Contacts':
            return ['id', 'First_Name', 'Last_Name', 'Email', 'Phone', 'Account_Name', 'Created_Time', 'Modified_Time']
        elif module == 'Accounts':
            return ['id', 'Account_Name', 'Account_Type', 'Industry', 'Annual_Revenue', 'Created_Time', 'Modified_Time']
        else:
            return ['id', 'Created_Time', 'Modified_Time']

def main():
    """Main function to execute bulk fetch operations"""
    try:
        # Initialize the SDK
        initialize_sdk()
        
        # Define modules to process
        modules = ['Deals', 'Accounts', 'Contacts', 'Leads']
        
        # Process each module
        for module_name in modules:
            try:
                logger.info(f"Processing {module_name} module...")
                
                # Get available fields for the module
                fields = get_module_fields(module_name)
                
                # Submit bulk read job
                logger.info(f"Submitting bulk read job for {module_name} module...")
                job_id = submit_bulk_read_job(module_name, fields)
                
                # Wait for job completion and download results
                if job_id:
                    logger.info(f"Waiting for job {job_id} to complete...")
                    wait_for_job_completion(job_id)
                    download_results(job_id)
                    
            except Exception as e:
                logger.error(f"Error processing {module_name} module: {str(e)}", exc_info=True)
                continue
            
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 