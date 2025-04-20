#!/usr/bin/env python3
"""
Script to transform Zoho CRM bulk read CSV data using the DataTransformer
"""

import sys
import os
import pandas as pd
from datetime import datetime
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root to Python path
try:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.insert(0, project_root)
    logger.info(f"Added project root to Python path: {project_root}")
    
    from backend.app.core.zoho.transformers import DataTransformer
    logger.info("Successfully imported DataTransformer")
except Exception as e:
    logger.error(f"Failed to set up environment: {str(e)}")
    sys.exit(1)

def transform_csv_data(csv_path):
    """
    Transform data from a Zoho CRM bulk read CSV file
    
    Args:
        csv_path (str): Path to the CSV file
        
    Returns:
        dict: Transformed data
    """
    try:
        # Read the CSV file
        logger.info(f"Reading CSV file: {csv_path}")
        df = pd.read_csv(csv_path)
        logger.info(f"Found {len(df)} records")
        
        # Show sample of columns
        logger.info(f"Columns in CSV: {', '.join(df.columns)}")
        
        # Convert DataFrame to list of dictionaries (format expected by transformer)
        records = df.to_dict('records')
        
        # Get module type from filename
        filename = os.path.basename(csv_path)
        if 'Deals' in filename:
            logger.info("Processing as Deals module")
            module_type = 'deals'
            transformed_data = DataTransformer.transform_deals(records)
        elif 'Accounts' in filename:
            logger.info("Processing as Accounts module")
            module_type = 'accounts'
            transformed_data = DataTransformer.transform_accounts(records)
        else:
            raise ValueError(f"Could not determine module type from filename: {filename}")
            
        # Add metadata
        result = {
            'module': module_type,
            'record_count': len(records),
            'transformed_at': datetime.now().isoformat(),
            'data': transformed_data
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error transforming data: {str(e)}", exc_info=True)
        return None

def main():
    try:
        if len(sys.argv) != 2:
            logger.error("Usage: python transform_data.py <path_to_csv>")
            sys.exit(1)
            
        csv_path = sys.argv[1]
        logger.info(f"Processing file: {csv_path}")
        
        if not os.path.exists(csv_path):
            logger.error(f"Error: File not found: {csv_path}")
            sys.exit(1)
            
        result = transform_csv_data(csv_path)
        if result:
            # Print formatted JSON output
            print(json.dumps(result, indent=2))
        else:
            logger.error("Failed to transform data")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main() 