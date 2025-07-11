#!/usr/bin/env python3
"""
CLI script to generate synthetic transaction data.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data_generation import generate_synthetic_data

def main():
    """Generate synthetic data."""
    print("🚀 Synthetic Data Generation")
    print("=" * 40)
    
    # Generate data
    customers_df, transactions_df = generate_synthetic_data(
        num_customers=100,
        num_transactions=1000,
        output_dir='data/raw'
    )
    
    print("\n✅ Data generation completed successfully!")

if __name__ == "__main__":
    main() 