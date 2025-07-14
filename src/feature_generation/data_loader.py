"""
Data Loading and Preprocessing Module

This module handles loading raw data from various sources and preprocessing
it for feature engineering.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional


def generate_sample_user_data(n_users: int = 1000) -> pd.DataFrame:
    """Generate sample user demographic data"""
    np.random.seed(42)
    
    # Generate user IDs
    user_ids = list(range(1, n_users + 1))
    
    # Generate demographic features
    ages = np.random.normal(35, 12, n_users).astype(int)
    ages = np.clip(ages, 18, 80)
    
    genders = np.random.choice(['M', 'F', 'Other'], n_users, p=[0.45, 0.45, 0.1])
    
    locations = np.random.choice([
        'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
        'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose'
    ], n_users)
    
    # Generate registration dates (last 2 years)
    start_date = datetime.now() - timedelta(days=730)
    registration_dates = [
        start_date + timedelta(days=np.random.randint(0, 730))
        for _ in range(n_users)
    ]
    
    # Generate premium status
    is_premium = np.random.choice([True, False], n_users, p=[0.2, 0.8])
    
    # Create DataFrame
    df = pd.DataFrame({
        'user_id': user_ids,
        'age': ages,
        'gender': genders,
        'location': locations,
        'registration_date': registration_dates,
        'is_premium': is_premium,
        'event_timestamp': datetime.now()
    })
    
    return df


def generate_sample_behavior_data(n_users: int = 1000, days: int = 30) -> pd.DataFrame:
    """Generate sample user behavior data"""
    np.random.seed(42)
    
    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    for user_id in range(1, n_users + 1):
        # Generate session data for each user
        n_sessions = np.random.poisson(15)  # Average 15 sessions per user
        
        for _ in range(n_sessions):
            session_date = start_date + timedelta(
                days=np.random.randint(0, days),
                hours=np.random.randint(0, 24),
                minutes=np.random.randint(0, 60)
            )
            
            session_duration = np.random.exponential(30)  # Average 30 minutes
            session_duration = min(session_duration, 180)  # Cap at 3 hours
            
            data.append({
                'user_id': user_id,
                'session_duration': session_duration,
                'session_date': session_date,
                'event_timestamp': session_date
            })
    
    df = pd.DataFrame(data)
    
    # Aggregate by user
    user_behavior = df.groupby('user_id').agg({
        'session_duration': ['mean', 'count'],
        'session_date': 'max'
    }).reset_index()
    
    user_behavior.columns = ['user_id', 'avg_session_duration', 'total_sessions', 'last_session_date']
    
    # Add additional features
    user_behavior['favorite_category'] = np.random.choice([
        'Electronics', 'Clothing', 'Books', 'Home', 'Sports'
    ], len(user_behavior))
    
    user_behavior['last_login_days'] = np.random.randint(0, 30, len(user_behavior))
    
    # Calculate engagement score (0-100)
    user_behavior['engagement_score'] = (
        user_behavior['avg_session_duration'] * 0.4 +
        user_behavior['total_sessions'] * 2 +
        (30 - user_behavior['last_login_days']) * 1.5
    ).clip(0, 100)
    
    user_behavior['event_timestamp'] = datetime.now()
    
    return user_behavior


def generate_sample_transaction_data(n_users: int = 1000, days: int = 365) -> pd.DataFrame:
    """Generate sample transaction data"""
    np.random.seed(42)
    
    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    for user_id in range(1, n_users + 1):
        # Generate transaction data for each user
        n_transactions = np.random.poisson(8)  # Average 8 transactions per user
        
        for _ in range(n_transactions):
            transaction_date = start_date + timedelta(
                days=np.random.randint(0, days),
                hours=np.random.randint(0, 24),
                minutes=np.random.randint(0, 60)
            )
            
            # Generate transaction amount (lognormal distribution)
            amount = np.random.lognormal(3.5, 0.8)  # Mean ~$50
            amount = min(amount, 1000)  # Cap at $1000
            
            payment_method = np.random.choice([
                'Credit Card', 'Debit Card', 'PayPal', 'Apple Pay', 'Google Pay'
            ], p=[0.4, 0.3, 0.15, 0.1, 0.05])
            
            data.append({
                'user_id': user_id,
                'amount': amount,
                'payment_method': payment_method,
                'transaction_date': transaction_date,
                'event_timestamp': transaction_date
            })
    
    df = pd.DataFrame(data)
    
    # Aggregate by user
    user_transactions = df.groupby('user_id').agg({
        'amount': ['sum', 'mean', 'count'],
        'payment_method': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Credit Card',
        'transaction_date': 'max'
    }).reset_index()
    
    user_transactions.columns = [
        'user_id', 'total_spent', 'avg_order_value', 'total_orders',
        'favorite_payment_method', 'last_purchase_date'
    ]
    
    # Calculate days since last purchase
    user_transactions['last_purchase_days'] = (
        end_date - user_transactions['last_purchase_date']
    ).dt.days
    
    user_transactions['event_timestamp'] = datetime.now()
    
    return user_transactions


def generate_sample_product_data(n_products: int = 500) -> pd.DataFrame:
    """Generate sample product data"""
    np.random.seed(42)
    
    # Generate product IDs
    product_ids = list(range(1, n_products + 1))
    
    # Generate product features
    categories = np.random.choice([
        'Electronics', 'Clothing', 'Books', 'Home', 'Sports',
        'Beauty', 'Toys', 'Automotive', 'Health', 'Garden'
    ], n_products)
    
    # Generate prices (lognormal distribution)
    prices = np.random.lognormal(3.2, 0.6)  # Mean ~$25
    prices = np.clip(prices, 5, 500)  # Between $5 and $500
    
    # Generate ratings (normal distribution)
    ratings = np.random.normal(4.2, 0.8, n_products)
    ratings = np.clip(ratings, 1, 5)
    
    # Generate review counts (poisson distribution)
    review_counts = np.random.poisson(50, n_products)
    review_counts = np.clip(review_counts, 0, 1000)
    
    # Generate inventory levels
    inventory_levels = np.random.poisson(100, n_products)
    inventory_levels = np.clip(inventory_levels, 0, 1000)
    
    # Create DataFrame
    df = pd.DataFrame({
        'product_id': product_ids,
        'category': categories,
        'price': prices,
        'avg_rating': ratings,
        'total_reviews': review_counts,
        'inventory_level': inventory_levels,
        'event_timestamp': datetime.now()
    })
    
    return df


def load_raw_data(data_dir: str = "data/raw") -> Dict[str, pd.DataFrame]:
    """
    Load raw data from files or generate sample data if files don't exist
    
    Args:
        data_dir: Directory containing raw data files
    
    Returns:
        Dictionary containing raw data DataFrames
    """
    raw_data = {}
    
    try:
        # Try to load existing files
        raw_data['users'] = pd.read_csv(f"{data_dir}/users.csv")
        raw_data['behavior'] = pd.read_csv(f"{data_dir}/user_behavior.csv")
        raw_data['transactions'] = pd.read_csv(f"{data_dir}/transactions.csv")
        raw_data['products'] = pd.read_csv(f"{data_dir}/products.csv")
        
        print("✅ Loaded existing raw data files")
        
    except FileNotFoundError:
        # Generate sample data if files don't exist
        print("📊 Generating sample data...")
        
        raw_data['users'] = generate_sample_user_data()
        raw_data['behavior'] = generate_sample_behavior_data()
        raw_data['transactions'] = generate_sample_transaction_data()
        raw_data['products'] = generate_sample_product_data()
        
        print("✅ Generated sample data")
    
    return raw_data


def validate_raw_data(raw_data: Dict[str, pd.DataFrame]) -> bool:
    """
    Validate raw data quality
    
    Args:
        raw_data: Dictionary containing raw data DataFrames
    
    Returns:
        bool: True if data is valid, False otherwise
    """
    try:
        for name, df in raw_data.items():
            print(f"📋 Validating {name} data:")
            print(f"  - Shape: {df.shape}")
            print(f"  - Missing values: {df.isnull().sum().sum()}")
            print(f"  - Duplicates: {df.duplicated().sum()}")
            
            if df.isnull().sum().sum() > 0:
                print(f"⚠️ Warning: {name} has missing values")
            
            if df.duplicated().sum() > 0:
                print(f"⚠️ Warning: {name} has duplicate rows")
        
        return True
        
    except Exception as e:
        print(f"❌ Data validation failed: {e}")
        return False 