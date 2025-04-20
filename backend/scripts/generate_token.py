"""
Script to generate refresh tokens from grant token using self_client.json and store them in .env
"""

import json
import os
from pathlib import Path
from zohocrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken
from zohocrmsdk.src.com.zoho.crm.api.dc import INDataCenter
from zohocrmsdk.src.com.zoho.crm.api.initializer import Initializer
from zohocrmsdk.src.com.zoho.crm.api.sdk_config import SDKConfig
from zohocrmsdk.src.com.zoho.api.logger import Logger
from dotenv import load_dotenv
from backend.app.core.zoho.token_store import EnvironmentTokenStore

def load_client_config():
    """Load client configuration from self_client.json"""
    try:
        with open(os.path.expanduser("~/Downloads/self_client.json"), "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading client config: {str(e)}")
        return None

def update_env_file(tokens):
    """Update .env file with tokens and configuration"""
    try:
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        
        # Prepare environment variables
        env_vars = {
            "ZOHO_CLIENT_ID": tokens['client_id'],
            "ZOHO_CLIENT_SECRET": tokens['client_secret'],
            "ZOHO_REFRESH_TOKEN": tokens['refresh_token'],
            "ZOHO_ACCESS_TOKEN": tokens['access_token'],
            "ZOHO_API_DOMAIN": tokens['api_domain']
        }

        # Write to .env file
        with open(env_path, "w") as f:
            f.write("# Zoho CRM API Configuration\n")
            f.write("# Client credentials\n")
            f.write(f"ZOHO_CLIENT_ID={env_vars['ZOHO_CLIENT_ID']}\n")
            f.write(f"ZOHO_CLIENT_SECRET={env_vars['ZOHO_CLIENT_SECRET']}\n\n")
            
            f.write("# Authentication tokens\n")
            f.write(f"ZOHO_REFRESH_TOKEN={env_vars['ZOHO_REFRESH_TOKEN']}\n")
            f.write(f"ZOHO_ACCESS_TOKEN={env_vars['ZOHO_ACCESS_TOKEN']}\n\n")
            
            f.write("# API Configuration\n")
            f.write(f"ZOHO_API_DOMAIN={env_vars['ZOHO_API_DOMAIN']}  # India datacenter\n\n")
            
            f.write("# Optional Configuration\n")
            f.write("# ZOHO_API_VERSION=v7\n")
            f.write("# ZOHO_DEBUG=false\n")
        
        print("Successfully updated .env file with tokens and configuration!")
    except Exception as e:
        print(f"Error updating .env file: {str(e)}")

def main():
    try:
        # Initialize logger
        Logger.get_instance(level=Logger.Levels.INFO, file_path="zoho_sdk.log")

        # Load client configuration
        client_config = load_client_config()

        # Initialize the SDK
        environment = INDataCenter.PRODUCTION()
        token = OAuthToken(
            client_id=client_config["client_id"],
            client_secret=client_config["client_secret"],
            grant_token=client_config["grant_token"],
            redirect_url="https://www.zoho.com/crm"
        )

        # Use the new environment-based token store
        store = EnvironmentTokenStore()
        config = SDKConfig()
        resource_path = os.path.join(os.path.dirname(__file__), ".")

        Initializer.initialize(
            user=None,
            environment=environment,
            token=token,
            store=store,
            sdk_config=config,
            resource_path=resource_path,
            logger=Logger.get_instance()
        )

        # Generate refresh token
        refresh_token = token.generate_refresh_token()
        print(f"Generated refresh token: {refresh_token}")

        # Update .env file
        update_env_file(refresh_token)
        print("Successfully updated .env file with the new refresh token")

    except Exception as e:
        print(f"Error generating token: {str(e)}")
        raise

if __name__ == "__main__":
    main() 