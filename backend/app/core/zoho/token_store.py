"""
Environment-based token store implementation for Zoho CRM
"""

import os
from typing import List, Optional
from zohocrmsdk.src.com.zoho.api.authenticator.store.token_store import TokenStore
from zohocrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken
from zohocrmsdk.src.com.zoho.crm.api.exception.sdk_exception import SDKException
from zohocrmsdk.src.com.zoho.crm.api.util.constants import Constants
from dotenv import load_dotenv

class EnvironmentTokenStore(TokenStore):
    """
    Token store implementation that uses environment variables for storage.
    This provides a more secure way to store tokens compared to file-based storage.
    """
    
    def __init__(self):
        """Initialize the environment token store"""
        load_dotenv()
    
    def find_token(self, token: OAuthToken) -> Optional[OAuthToken]:
        """
        Find a token in the environment variables
        
        Args:
            token: The OAuth token to find
            
        Returns:
            The found token or None if not found
        """
        if not isinstance(token, OAuthToken):
            return token
            
        try:
            # Get token details from environment
            client_id = os.getenv('ZOHO_CLIENT_ID')
            client_secret = os.getenv('ZOHO_CLIENT_SECRET')
            refresh_token = os.getenv('ZOHO_REFRESH_TOKEN')
            access_token = os.getenv('ZOHO_ACCESS_TOKEN')
            api_domain = os.getenv('ZOHO_API_DOMAIN')
            
            # If we have the required tokens, set them on the token object
            if all([client_id, client_secret, refresh_token]):
                token.set_client_id(client_id)
                token.set_client_secret(client_secret)
                token.set_refresh_token(refresh_token)
                if access_token:
                    token.set_access_token(access_token)
                if api_domain:
                    token.set_api_domain(api_domain)
                return token
                
            return None
            
        except Exception as ex:
            raise SDKException(code=Constants.TOKEN_STORE, 
                             message="Error finding token in environment", 
                             cause=ex)
    
    def save_token(self, token: OAuthToken) -> None:
        """
        Save a token to environment variables
        
        Args:
            token: The OAuth token to save
        """
        if not isinstance(token, OAuthToken):
            return
            
        try:
            # Update environment variables with token details
            if token.get_client_id():
                os.environ['ZOHO_CLIENT_ID'] = token.get_client_id()
            if token.get_client_secret():
                os.environ['ZOHO_CLIENT_SECRET'] = token.get_client_secret()
            if token.get_refresh_token():
                os.environ['ZOHO_REFRESH_TOKEN'] = token.get_refresh_token()
            if token.get_access_token():
                os.environ['ZOHO_ACCESS_TOKEN'] = token.get_access_token()
            if token.get_api_domain():
                os.environ['ZOHO_API_DOMAIN'] = token.get_api_domain()
                
        except Exception as ex:
            raise SDKException(code=Constants.TOKEN_STORE,
                             message="Error saving token to environment",
                             cause=ex)
    
    def delete_token(self, id: str) -> None:
        """
        Delete a token from environment variables
        
        Args:
            id: The token ID to delete
        """
        try:
            # Clear all Zoho-related environment variables
            os.environ.pop('ZOHO_CLIENT_ID', None)
            os.environ.pop('ZOHO_CLIENT_SECRET', None)
            os.environ.pop('ZOHO_REFRESH_TOKEN', None)
            os.environ.pop('ZOHO_ACCESS_TOKEN', None)
            os.environ.pop('ZOHO_API_DOMAIN', None)
            
        except Exception as ex:
            raise SDKException(code=Constants.TOKEN_STORE,
                             message="Error deleting token from environment",
                             cause=ex)
    
    def get_tokens(self) -> List[OAuthToken]:
        """
        Get all tokens from environment variables
        
        Returns:
            List of OAuth tokens
        """
        tokens = []
        try:
            # Create a token from environment variables if they exist
            client_id = os.getenv('ZOHO_CLIENT_ID')
            client_secret = os.getenv('ZOHO_CLIENT_SECRET')
            refresh_token = os.getenv('ZOHO_REFRESH_TOKEN')
            
            if all([client_id, client_secret, refresh_token]):
                token = OAuthToken(
                    client_id=client_id,
                    client_secret=client_secret,
                    refresh_token=refresh_token
                )
                if os.getenv('ZOHO_ACCESS_TOKEN'):
                    token.set_access_token(os.getenv('ZOHO_ACCESS_TOKEN'))
                if os.getenv('ZOHO_API_DOMAIN'):
                    token.set_api_domain(os.getenv('ZOHO_API_DOMAIN'))
                tokens.append(token)
                
            return tokens
            
        except Exception as ex:
            raise SDKException(code=Constants.TOKEN_STORE,
                             message="Error getting tokens from environment",
                             cause=ex)
    
    def delete_tokens(self) -> None:
        """Delete all tokens from environment variables"""
        try:
            # Clear all Zoho-related environment variables
            os.environ.pop('ZOHO_CLIENT_ID', None)
            os.environ.pop('ZOHO_CLIENT_SECRET', None)
            os.environ.pop('ZOHO_REFRESH_TOKEN', None)
            os.environ.pop('ZOHO_ACCESS_TOKEN', None)
            os.environ.pop('ZOHO_API_DOMAIN', None)
            
        except Exception as ex:
            raise SDKException(code=Constants.TOKEN_STORE,
                             message="Error deleting tokens from environment",
                             cause=ex)
    
    def find_token_by_id(self, id: str) -> Optional[OAuthToken]:
        """
        Find a token by ID in environment variables
        
        Args:
            id: The token ID to find
            
        Returns:
            The found token or None if not found
        """
        try:
            # Since we only store one set of credentials in environment,
            # we can just return the token if it exists
            return self.get_tokens()[0] if self.get_tokens() else None
            
        except Exception as ex:
            raise SDKException(code=Constants.TOKEN_STORE,
                             message="Error finding token by ID in environment",
                             cause=ex) 