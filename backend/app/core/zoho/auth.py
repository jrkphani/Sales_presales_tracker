"""
Zoho Authentication Module
Handles OAuth2 authentication with Zoho API using the official SDK
"""

import logging
from zohocrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken
from zohocrmsdk.src.com.zoho.crm.api.dc.data_center import INDataCenter
from zohocrmsdk.src.com.zoho.api.logger import Logger
from zohocrmsdk.src.com.zoho.crm.api.sdk_config import SDKConfig
from zohocrmsdk.src.com.zoho.crm.api.initializer import Initializer
from flask import current_app
from backend.app.core.zoho.token_store import EnvironmentTokenStore

logger = logging.getLogger(__name__)

class ZohoAuth:
    """Handles Zoho API authentication using the official SDK"""
    
    def __init__(self):
        self.config = current_app.config['ZOHO_API']
        self._initialize_sdk()
    
    def _initialize_sdk(self):
        """Initialize the Zoho CRM SDK"""
        try:
            # Create OAuth token
            token = OAuthToken(
                client_id=self.config['client_id'],
                client_secret=self.config['client_secret'],
                refresh_token=self.config['refresh_token']
            )
            
            # Use the new environment-based token store
            store = EnvironmentTokenStore()
            
            # Initialize the SDK
            Initializer.initialize(
                environment=INDataCenter.PRODUCTION(),
                token=token,
                store=store,
                sdk_config=SDKConfig(auto_refresh_fields=True, pick_list_validation=False)
            )
            
            logger.info('Zoho CRM SDK initialized successfully')
            
        except Exception as e:
            logger.error(f'Failed to initialize Zoho CRM SDK: {str(e)}')
            raise
    
    def get_access_token(self):
        """
        Get a valid access token using the refresh token
        Returns the access token string
        """
        try:
            # The SDK handles token refresh automatically
            # We just need to get the current token
            token = Initializer.get_initializer().get_token()
            return token.get_access_token()
            
        except Exception as e:
            logger.error(f'Failed to get access token: {str(e)}')
            raise

    def invalidate_token(self):
        """Invalidate the current access token"""
        try:
            # The SDK handles token invalidation automatically
            # We just need to reinitialize
            self._initialize_sdk()
        except Exception as e:
            logger.error(f'Failed to invalidate token: {str(e)}')
            raise 