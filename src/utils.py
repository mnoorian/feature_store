import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple

def load_data(customers_path: str = 'data/raw/customers.csv', 
              transactions_path: str = 'data/raw/transactions.csv') -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load customers and transactions data."""
    customers_df = pd.read_csv(customers_path)
    transactions_df = pd.read_csv(transactions_path)
    
    # Convert transaction_date to datetime
    transactions_df['transaction_date'] = pd.to_datetime(transactions_df['transaction_date'])
    transactions_df = transactions_df.sort_values(['customer_id', 'transaction_date'])
    
    print(f"📊 Loaded {len(customers_df)} customers and {len(transactions_df)} transactions")
    return customers_df, transactions_df

def analyze_features(final_features: pd.DataFrame) -> pd.DataFrame:
    """Analyze and print key statistics and segment analysis."""
    key_features = [
        'total_transactions_12m', 'avg_transactions_per_month',
        'total_amount_12m', 'avg_amount_12m',
        'purchase_count_12m', 'withdrawal_count_12m',
        'purchase_amount_12m', 'withdrawal_amount_12m'
    ]
    
    print("\n📊 KEY FEATURES STATISTICS:")
    print("=" * 50)
    print(final_features[key_features].describe())
    
    segment_analysis = final_features.groupby('customer_segment').agg({
        'customer_id': 'count',
        'total_amount_12m': ['mean', 'sum'],
        'total_transactions_12m': 'mean',
        'avg_amount_12m': 'mean',
        'credit_score': 'mean'
    }).round(2)
    
    segment_analysis.columns = ['customer_count', 'avg_total_amount', 'total_amount_sum', 
                               'avg_transactions', 'avg_amount', 'avg_credit_score']
    
    print("\n📊 CUSTOMER SEGMENTATION ANALYSIS:")
    print("=" * 60)
    print(segment_analysis)
    
    return segment_analysis

def visualize_features(final_features: pd.DataFrame, segment_analysis: pd.DataFrame) -> None:
    """Create summary plots for features and segments."""
    plt.style.use('default')
    sns.set_palette("husl")
    
    plt.figure(figsize=(15, 10))
    
    # Distribution of average transactions per month
    plt.subplot(2, 3, 1)
    plt.hist(final_features['avg_transactions_per_month'], bins=30, alpha=0.7, color='skyblue')
    plt.title('Distribution of Avg Transactions per Month')
    plt.xlabel('Avg Transactions per Month')
    plt.ylabel('Count')
    
    # Distribution of average amount
    plt.subplot(2, 3, 2)
    plt.hist(final_features['avg_amount_12m'], bins=30, alpha=0.7, color='lightgreen')
    plt.title('Distribution of Avg Transaction Amount (12m)')
    plt.xlabel('Avg Amount ($)')
    plt.ylabel('Count')
    
    # Scatter plot
    plt.subplot(2, 3, 3)
    plt.scatter(final_features['total_transactions_12m'], final_features['total_amount_12m'], alpha=0.6)
    plt.title('Transactions vs Total Amount (12m)')
    plt.xlabel('Total Transactions')
    plt.ylabel('Total Amount ($)')
    
    # Transaction type distribution
    plt.subplot(2, 3, 4)
    transaction_types = ['purchase_count_12m', 'withdrawal_count_12m', 'transfer_count_12m', 'deposit_count_12m']
    transaction_data = [final_features[col].sum() for col in transaction_types]
    plt.pie(transaction_data, labels=['Purchase', 'Withdrawal', 'Transfer', 'Deposit'], autopct='%1.1f%%')
    plt.title('Transaction Type Distribution (12m)')
    
    # Customer segment distribution
    plt.subplot(2, 3, 5)
    segment_counts = final_features['customer_segment'].value_counts()
    plt.pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%')
    plt.title('Customer Segment Distribution')
    
    # Average amount by segment
    plt.subplot(2, 3, 6)
    segment_analysis['avg_total_amount'].plot(kind='bar', color='lightcoral')
    plt.title('Average Total Amount by Segment')
    plt.xlabel('Segment')
    plt.ylabel('Avg Amount ($)')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()

def export_results(final_features: pd.DataFrame, segment_analysis: pd.DataFrame, 
                   output_dir: str = 'data/transformed') -> None:
    """Export features and segment analysis to CSV."""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    final_features.to_csv(f'{output_dir}/customer_features_12months.csv', index=False)
    segment_analysis.to_csv(f'{output_dir}/customer_segments_analysis.csv')
    
    print("✅ Features exported to 'customer_features_12months.csv'")
    print("✅ Segment analysis exported to 'customer_segments_analysis.csv'")

def print_summary(final_features: pd.DataFrame) -> None:
    """Print summary statistics."""
    print(f"\n📊 SUMMARY:")
    print(f"  - Total customers: {len(final_features)}")
    print(f"  - Features generated: {len(final_features.columns)}")
    print(f"  - Date range: {final_features['latest_transaction_date'].min()} to {final_features['latest_transaction_date'].max()}")
    print(f"  - Active customers (12m): {len(final_features[final_features['total_transactions_12m'] > 0])}")
    print(f"  - Inactive customers: {len(final_features[final_features['total_transactions_12m'] == 0])}")
    
    print(f"\n📋 SAMPLE FEATURES:")
    print(final_features.head()) 