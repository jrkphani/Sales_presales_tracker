"""
Data Transformation Module
Handles transformation of raw Zoho CRM data into the required format
"""

import logging
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)

class DataTransformer:
    """Transform raw Zoho CRM data into dashboard format"""
    
    @staticmethod
    def transform_deals(deals_data, currency_info=None):
        """Transform raw deals data into dashboard format
        
        Args:
            deals_data (list): List of raw deal records from Zoho CRM
            currency_info (dict, optional): Currency information containing:
                - code: Currency code (e.g. 'USD')
                - symbol: Currency symbol (e.g. '$')
                - name: Currency name (e.g. 'US Dollar')
                
        Returns:
            dict: Transformed deals data with metrics and currency info
        """
        try:
            if not deals_data:
                return {
                    'total_deals': 0,
                    'total_value': 0,
                    'avg_deal_size': 0,
                    'stages': {},
                    'monthly_trends': {},
                    'win_rate': 0,
                    'currency': currency_info or {'code': 'USD', 'symbol': '$', 'name': 'US Dollar'}
                }

            # Convert to DataFrame
            df = pd.DataFrame(deals_data)
            
            # Calculate metrics
            total_deals = len(df)
            total_value = df['Amount'].sum()
            avg_deal_size = total_value / total_deals if total_deals > 0 else 0
            
            # Get stage distribution
            stages = df['Stage'].value_counts().to_dict()
            
            # Calculate win rate
            closed_won = df[df['Stage'] == 'Closed Won'].shape[0]
            win_rate = (closed_won / total_deals) * 100 if total_deals > 0 else 0
            
            # Get monthly trends
            df['Closing_Date'] = pd.to_datetime(df['Closing_Date'])
            monthly = df.groupby(df['Closing_Date'].dt.strftime('%Y-%m'))[['Amount']].sum()
            monthly_trends = monthly.to_dict()['Amount']
            
            return {
                'total_deals': total_deals,
                'total_value': total_value,
                'avg_deal_size': avg_deal_size,
                'stages': stages,
                'monthly_trends': monthly_trends,
                'win_rate': win_rate,
                'currency': currency_info or {'code': 'USD', 'symbol': '$', 'name': 'US Dollar'}
            }
            
        except Exception as e:
            logger.error(f"Error transforming deals data: {str(e)}")
            return {
                'total_deals': 0,
                'total_value': 0,
                'avg_deal_size': 0,
                'stages': {},
                'monthly_trends': {},
                'win_rate': 0,
                'currency': currency_info or {'code': 'USD', 'symbol': '$', 'name': 'US Dollar'}
            }
    
    @staticmethod
    def transform_accounts(accounts_data):
        """
        Transform accounts data for dashboard
        
        Args:
            accounts_data (list): Raw accounts data from Zoho
            
        Returns:
            dict: Transformed accounts data
        """
        try:
            df = pd.DataFrame(accounts_data)
            
            # Industry distribution
            industry_distribution = df['Industry'].value_counts().to_dict()
            
            # Account types
            account_types = df['Account_Type'].value_counts().to_dict()
            
            return {
                'industry_distribution': industry_distribution,
                'account_types': account_types,
                'total_accounts': len(df)
            }
            
        except Exception as e:
            logger.error(f'Failed to transform accounts data: {str(e)}')
            raise
    
    @staticmethod
    def combine_dashboard_data(deals_data, accounts_data, currency_info=None):
        """Combine transformed deals and accounts data
        
        Args:
            deals_data (dict): Transformed deals data
            accounts_data (dict): Transformed accounts data
            currency_info (dict, optional): Currency information
            
        Returns:
            dict: Combined dashboard data with timestamp
        """
        # Add currency info to deals data if not already present
        if currency_info and 'currency' not in deals_data:
            deals_data['currency'] = currency_info
            
        return {
            'deals': deals_data,
            'accounts': accounts_data,
            'last_updated': datetime.now().isoformat()
        } 