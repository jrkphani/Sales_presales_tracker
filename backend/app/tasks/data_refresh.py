"""
Data Refresh Task Module
Handles periodic data refresh from Zoho CRM
"""

import logging
from app.core.services.data_service import DataService

logger = logging.getLogger(__name__)

def refresh_data():
    """
    Refresh data from Zoho CRM
    This function is called periodically by the scheduler
    """
    try:
        logger.info('Starting scheduled data refresh...')
        
        # Create service instance
        service = DataService()
        
        # Fetch and process data
        data = service.fetch_all_data()
        
        logger.info('Scheduled data refresh completed successfully')
        return data
        
    except Exception as e:
        logger.error(f'Scheduled data refresh failed: {str(e)}')
        raise 