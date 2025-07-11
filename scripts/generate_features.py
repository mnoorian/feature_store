#!/usr/bin/env python3
"""
CLI script to generate 12-month rolling features from transaction data.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.feature_engineering import filter_completed_transactions, generate_12month_features, segment_customers
from src.utils import load_data, analyze_features, visualize_features, export_results, print_summary

def main():
    """Generate 12-month rolling features."""
    print("🚀 12-Month Rolling Feature Engineering")
    print("=" * 60)
    
    # Load data
    customers_df, transactions_df = load_data()
    
    # Filter completed transactions
    completed_tx = filter_completed_transactions(transactions_df)
    print(f"✅ Total transactions: {len(transactions_df)}")
    print(f"✅ Completed transactions: {len(completed_tx)}")
    print(f"📅 Date range: {transactions_df['transaction_date'].min()} to {transactions_df['transaction_date'].max()}")
    
    # Generate features
    print("\n🔄 Generating 12-month rolling features...")
    features_df = generate_12month_features(completed_tx)
    print(f"✅ Generated features for {len(features_df)} customers")
    
    # Merge with customer data
    final_features = customers_df.merge(features_df, on='customer_id', how='left')
    
    # Fill NaN values for customers with no transactions
    numeric_columns = final_features.select_dtypes(include=['number']).columns
    final_features[numeric_columns] = final_features[numeric_columns].fillna(0)
    
    # Add segmentation
    final_features['customer_segment'] = segment_customers(final_features)
    
    # Analyze and visualize
    segment_analysis = analyze_features(final_features)
    visualize_features(final_features, segment_analysis)
    
    # Export results
    export_results(final_features, segment_analysis)
    
    # Print summary
    print_summary(final_features)

if __name__ == "__main__":
    main() 