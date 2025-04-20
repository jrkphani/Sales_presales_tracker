"""
Script to generate refresh token from grant token using Zoho CRM SDK
"""

import os
from dotenv import load_dotenv
from zohocrmsdk.src.com.zoho.crm.api.user_signature import UserSignature
from zohocrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken
from zohocrmsdk.src.com.zoho.crm.api.dc import USDataCenter
from zohocrmsdk.src.com.zoho.crm.api.initializer import Initializer
from backend.app.core.zoho.token_store import EnvironmentTokenStore

def generate_refresh_token():
    """
    Generate refresh token from grant token using Zoho CRM SDK
    """
    try:
        # Load environment variables
        load_dotenv()
        
        # Get credentials from environment
        client_id = os.getenv('ZOHO_CLIENT_ID')
        client_secret = os.getenv('ZOHO_CLIENT_SECRET')
        grant_token = os.getenv('ZOHO_GRANT_TOKEN')
        
        if not all([client_id, client_secret, grant_token]):
            print("Error: Missing required environment variables")
            print("Please ensure ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, and ZOHO_GRANT_TOKEN are set in .env")
            return
        
        # Configure environment
        environment = USDataCenter.PRODUCTION()
        
        # Create OAuthToken instance
        token = OAuthToken(
            client_id=client_id,
            client_secret=client_secret,
            grant_token=grant_token,
            redirect_url='https://www.zoho.com'  # Default redirect URL
        )
        
        # Use the new environment-based token store
        store = EnvironmentTokenStore()
        
        # Initialize the SDK
        Initializer.initialize(environment=environment, token=token, store=store)
        
        # Generate tokens
        token.generate_token()
        
        # Get the refresh token
        refresh_token = token.refresh_token
        
        print("\nRefresh Token generated successfully!")
        print(f"Refresh Token: {refresh_token}")
        print("\nPlease update your .env file with this refresh token:")
        print(f"ZOHO_REFRESH_TOKEN={refresh_token}")
        
    except Exception as e:
        print(f"Error generating refresh token: {str(e)}")
        raise

if __name__ == "__main__":
    generate_refresh_token() 