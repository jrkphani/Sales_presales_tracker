"""
Dashboard Service Module
Handles dashboard data preparation and caching
"""

import logging
import json
import os
from datetime import datetime, timedelta
from flask import current_app
from app.core.services.data_service import DataService

logger = logging.getLogger(__name__)

class DashboardService:
    """Service for handling dashboard data operations"""
    
    def __init__(self):
        self.data_service = DataService()
    
    def get_dashboard_data(self):
        """
        Get dashboard data, refreshing if necessary
        Returns processed data ready for dashboard
        """
        try:
            current_data = self._load_current_data()
            
            # Check if data needs refresh
            if self._needs_refresh(current_data):
                logger.info('Dashboard data needs refresh, fetching new data...')
                return self.data_service.fetch_all_data()
            
            return current_data
            
        except Exception as e:
            logger.error(f'Failed to get dashboard data: {str(e)}')
            raise
    
    def _load_current_data(self):
        """Load current data from file"""
        data_path = current_app.config['DATA']['current_data_path']
        
        if not os.path.exists(data_path):
            return None
            
        try:
            with open(data_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f'Failed to load current data: {str(e)}')
            return None
    
    def _needs_refresh(self, current_data):
        """Check if data needs to be refreshed"""
        if not current_data:
            return True
            
        # Get refresh interval from config
        refresh_interval = current_app.config['DATA']['refresh_interval']
        
        # Check last update time
        last_updated = current_data.get('last_updated')
        if not last_updated:
            return True
            
        try:
            last_update_time = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
            refresh_time = datetime.utcnow() - timedelta(hours=refresh_interval)
            return last_update_time < refresh_time
            
        except (ValueError, AttributeError) as e:
            logger.error(f'Failed to parse last update time: {str(e)}')
            return True

def get_dashboard_data():
    """Get dashboard data for API endpoint"""
    service = DashboardService()
    return service.get_dashboard_data() 