import pandas as pd
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any

def generate_customers(num_customers: int = 100) -> pd.DataFrame:
    """Generate synthetic customer data."""
    customers = []
    
    for i in range(num_customers):
        customer = {
            'customer_id': str(uuid.uuid4()),
            'first_name': random.choice(['John', 'Jane', 'Mike', 'Sarah', 'David', 'Lisa', 'Tom', 'Emma', 'Alex', 'Maria']),
            'last_name': random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']),
            'email': f"customer{i+1}@example.com",
            'phone': f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            'address': f"{random.randint(100, 9999)} {random.choice(['Main St', 'Oak Ave', 'Pine Rd', 'Elm St', 'Maple Dr'])}",
            'city': random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']),
            'state': random.choice(['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'FL', 'OH', 'GA', 'NC']),
            'zip_code': f"{random.randint(10000, 99999)}",
            'credit_score': random.randint(300, 850),
            'annual_income': random.randint(20000, 200000),
            'account_status': random.choice(['active', 'inactive', 'suspended'])
        }
        customers.append(customer)
    
    return pd.DataFrame(customers)

def generate_transactions(customers_df: pd.DataFrame, num_transactions: int = 1000) -> pd.DataFrame:
    """Generate synthetic transaction data."""
    transactions = []
    customer_ids = customers_df['customer_id'].tolist()
    
    # Generate transactions over the past year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    for i in range(num_transactions):
        # Random transaction date within the past year
        days_ago = random.randint(0, 365)
        transaction_date = end_date - timedelta(days=days_ago)
        
        transaction = {
            'transaction_id': str(uuid.uuid4()),
            'customer_id': random.choice(customer_ids),
            'transaction_type': random.choice(['purchase', 'withdrawal', 'transfer', 'deposit']),
            'amount': round(random.uniform(10, 2000), 2),
            'currency': 'USD',
            'transaction_date': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
            'merchant_name': random.choice(['Walmart', 'Amazon', 'Target', 'Home Depot', 'Best Buy', 'Costco', 'Kroger', 'Walgreens', 'CVS', 'McDonald\'s']),
            'merchant_category': random.choice(['retail', 'food', 'gas', 'entertainment', 'utilities', 'healthcare', 'transportation', 'education', 'travel', 'other']),
            'status': random.choice(['completed', 'pending', 'failed', 'cancelled']),
            'description': f"Transaction {i+1}",
            'reference_number': f"REF{random.randint(100000, 999999)}",
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        transactions.append(transaction)
    
    return pd.DataFrame(transactions)

def save_data_to_csv(customers_df: pd.DataFrame, transactions_df: pd.DataFrame, output_dir: str = 'output') -> None:
    """Save generated data to CSV files."""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    customers_df.to_csv(f'{output_dir}/customers.csv', index=False)
    transactions_df.to_csv(f'{output_dir}/transactions.csv', index=False)
    
    print(f"✅ Generated {len(customers_df)} customers")
    print(f"✅ Generated {len(transactions_df)} transactions")
    print(f"✅ Data saved to {output_dir}/")

def generate_synthetic_data(num_customers: int = 100, num_transactions: int = 1000, output_dir: str = 'output') -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generate complete synthetic dataset."""
    print("🔄 Generating synthetic customer data...")
    customers_df = generate_customers(num_customers)
    
    print("🔄 Generating synthetic transaction data...")
    transactions_df = generate_transactions(customers_df, num_transactions)
    
    print("💾 Saving data to CSV files...")
    save_data_to_csv(customers_df, transactions_df, output_dir)
    
    return customers_df, transactions_df 