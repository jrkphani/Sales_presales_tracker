"""
Task Scheduler Module
Handles scheduling and execution of background tasks
"""

import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import current_app
from app.tasks.data_refresh import refresh_data

logger = logging.getLogger(__name__)

def init_scheduler(app):
    """
    Initialize the task scheduler
    
    Args:
        app: Flask application instance
        
    Returns:
        BackgroundScheduler: Configured scheduler instance
    """
    try:
        # Create scheduler
        scheduler = BackgroundScheduler()
        
        # Get refresh interval from config
        refresh_interval = app.config['DATA']['refresh_interval']
        
        # Add data refresh job
        scheduler.add_job(
            func=refresh_data,
            trigger=IntervalTrigger(hours=refresh_interval),
            id='data_refresh',
            name='Refresh Zoho CRM data',
            replace_existing=True
        )
        
        # Add error listener
        scheduler.add_listener(
            _handle_job_error,
            'job_error'
        )
        
        logger.info(f'Scheduler initialized with {refresh_interval}h refresh interval')
        return scheduler
        
    except Exception as e:
        logger.error(f'Failed to initialize scheduler: {str(e)}')
        raise

def _handle_job_error(event):
    """Handle job execution errors"""
    logger.error(f'Job {event.job_id} failed: {str(event.exception)}') 