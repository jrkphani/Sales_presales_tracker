"""
Dashboard Data Preparation Script
Processes raw CSV data and prepares it for dashboard visualization
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime

class DataTransformer:
    """Transforms raw Zoho CRM data into the required format"""
    
    @staticmethod
    def transform_deals(deals_data):
        """
        Transform deals data for dashboard
        
        Args:
            deals_data (list): Raw deals data from Zoho
            
        Returns:
            dict: Transformed data with various metrics
        """
        try:
            # Convert to DataFrame for easier manipulation
            df = pd.DataFrame(deals_data)
            
            # Calculate basic metrics
            total_deals = len(df)
            total_value = df['Amount'].fillna(0).sum()
            avg_deal_size = total_value / total_deals if total_deals > 0 else 0
            
            # Deal stages analysis
            stage_distribution = df['Stage'].value_counts().to_dict()
            
            # Monthly trends
            df['Closing_Date'] = pd.to_datetime(df['Closing_Date'])
            monthly_deals = df.groupby(df['Closing_Date'].dt.strftime('%Y-%m'))[['Amount']].agg({
                'Amount': 'sum',
                'count': 'size'
            }).to_dict('index')
            
            # Win rate calculation
            won_deals = len(df[df['Stage'] == 'Closed Won'])
            win_rate = (won_deals / total_deals * 100) if total_deals > 0 else 0
            
            return {
                'metrics': {
                    'total_deals': total_deals,
                    'total_value': total_value,
                    'avg_deal_size': avg_deal_size,
                    'win_rate': win_rate
                },
                'stage_distribution': stage_distribution,
                'monthly_trends': monthly_deals
            }
            
        except Exception as e:
            print(f'Failed to transform deals data: {str(e)}')
            raise
    
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
            industry_distribution = df['Industry'].fillna('Unknown').value_counts().to_dict()
            
            # Account types
            account_types = df['Account_Type'].fillna('Unknown').value_counts().to_dict()
            
            return {
                'industry_distribution': industry_distribution,
                'account_types': account_types,
                'total_accounts': len(df)
            }
            
        except Exception as e:
            print(f'Failed to transform accounts data: {str(e)}')
            raise
    
    @staticmethod
    def combine_dashboard_data(deals_data, accounts_data):
        """
        Combine transformed data for dashboard
        
        Args:
            deals_data (dict): Transformed deals data
            accounts_data (dict): Transformed accounts data
            
        Returns:
            dict: Combined dashboard data
        """
        return {
            'deals': deals_data,
            'accounts': accounts_data,
            'last_updated': datetime.utcnow().isoformat()
        }

def load_csv_data(file_path):
    """Load data from CSV file"""
    return pd.read_csv(file_path).to_dict('records')

def save_dashboard_data(data, output_path):
    """Save transformed data to JSON file"""
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    # Initialize paths
    data_dir = Path('backend/data')
    output_dir = Path('backend/data/dashboard')
    output_dir.mkdir(exist_ok=True)
    
    # Load data from CSV files
    deals_data = load_csv_data(data_dir / 'bulk_read_495490000013193038.csv')
    accounts_data = load_csv_data(data_dir / 'bulk_read_495490000013192045.csv')
    contacts_data = load_csv_data(data_dir / 'bulk_read_495490000013190027.csv')
    
    # Transform data
    transformer = DataTransformer()
    
    # Transform deals data
    deals_metrics = transformer.transform_deals(deals_data)
    
    # Transform accounts data
    accounts_metrics = transformer.transform_accounts(accounts_data)
    
    # Combine data for dashboard
    dashboard_data = transformer.combine_dashboard_data(deals_metrics, accounts_metrics)
    
    # Add contacts summary
    dashboard_data['contacts'] = {
        'total_contacts': len(contacts_data),
        'last_updated': datetime.utcnow().isoformat()
    }
    
    # Save to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f'dashboard_data_{timestamp}.json'
    save_dashboard_data(dashboard_data, output_file)
    
    print(f"Dashboard data prepared and saved to: {output_file}")
    print("\nSummary:")
    print(f"Total Deals: {deals_metrics['metrics']['total_deals']}")
    print(f"Total Value: ${deals_metrics['metrics']['total_value']:,.2f}")
    print(f"Win Rate: {deals_metrics['metrics']['win_rate']:.1f}%")
    print(f"Total Accounts: {accounts_metrics['total_accounts']}")
    print(f"Total Contacts: {len(contacts_data)}")

if __name__ == '__main__':
    main() 