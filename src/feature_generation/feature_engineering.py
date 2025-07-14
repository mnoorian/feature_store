"""
Feature Engineering Module

This module contains all feature engineering logic for transforming raw data
into features suitable for ML models.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional


def engineer_user_demographic_features(users_df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer user demographic features
    
    Args:
        users_df: Raw user data DataFrame
    
    Returns:
        DataFrame with engineered demographic features
    """
    print("🔧 Engineering user demographic features...")
    
    # Create a copy to avoid modifying original data
    features = users_df.copy()
    
    # Convert registration_date to datetime if it's a string
    if features['registration_date'].dtype == 'object':
        features['registration_date'] = pd.to_datetime(features['registration_date'])
    
    # Calculate user tenure (days since registration)
    features['user_tenure_days'] = (
        datetime.now() - features['registration_date']
    ).dt.days
    
    # Create age groups
    features['age_group'] = pd.cut(
        features['age'],
        bins=[0, 25, 35, 45, 55, 100],
        labels=['18-25', '26-35', '36-45', '46-55', '55+']
    )
    
    # Create location groups (major cities vs others)
    major_cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
    features['is_major_city'] = features['location'].isin(major_cities)
    
    # Create gender encoding
    features['gender_encoded'] = features['gender'].map({'M': 1, 'F': 2, 'Other': 3})
    
    # Calculate registration month and day of week
    features['registration_month'] = features['registration_date'].dt.month
    features['registration_day_of_week'] = features['registration_date'].dt.dayofweek
    
    # Create premium user flag
    features['is_premium'] = features['is_premium'].astype(int)
    
    # Select final features for feature store
    final_features = features[[
        'user_id', 'age', 'gender', 'location', 'registration_date',
        'is_premium', 'event_timestamp'
    ]].copy()
    
    print(f"✅ Engineered {len(final_features)} user demographic features")
    return final_features


def engineer_user_behavior_features(behavior_df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer user behavior features
    
    Args:
        behavior_df: Raw user behavior data DataFrame
    
    Returns:
        DataFrame with engineered behavior features
    """
    print("🔧 Engineering user behavior features...")
    
    # Create a copy to avoid modifying original data
    features = behavior_df.copy()
    
    # Convert session date to datetime if it's a string
    if 'last_session_date' in features.columns and features['last_session_date'].dtype == 'object':
        features['last_session_date'] = pd.to_datetime(features['last_session_date'])
    
    # Create session frequency categories
    features['session_frequency'] = pd.cut(
        features['total_sessions'],
        bins=[0, 5, 15, 30, 1000],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    
    # Create session duration categories
    features['session_duration_category'] = pd.cut(
        features['avg_session_duration'],
        bins=[0, 15, 30, 60, 1000],
        labels=['Short', 'Medium', 'Long', 'Very Long']
    )
    
    # Create engagement level based on engagement score
    features['engagement_level'] = pd.cut(
        features['engagement_score'],
        bins=[0, 25, 50, 75, 100],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    
    # Create activity recency categories
    features['activity_recency'] = pd.cut(
        features['last_login_days'],
        bins=[0, 1, 7, 30, 1000],
        labels=['Very Recent', 'Recent', 'Moderate', 'Inactive']
    )
    
    # Create favorite category encoding
    category_mapping = {
        'Electronics': 1, 'Clothing': 2, 'Books': 3, 'Home': 4, 'Sports': 5
    }
    features['favorite_category_encoded'] = features['favorite_category'].map(category_mapping)
    
    # Select final features for feature store
    final_features = features[[
        'user_id', 'avg_session_duration', 'total_sessions', 'favorite_category',
        'last_login_days', 'engagement_score', 'event_timestamp'
    ]].copy()
    
    print(f"✅ Engineered {len(final_features)} user behavior features")
    return final_features


def engineer_transaction_features(transactions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer transaction features
    
    Args:
        transactions_df: Raw transaction data DataFrame
    
    Returns:
        DataFrame with engineered transaction features
    """
    print("🔧 Engineering transaction features...")
    
    # Create a copy to avoid modifying original data
    features = transactions_df.copy()
    
    # Convert purchase date to datetime if it's a string
    if 'last_purchase_date' in features.columns and features['last_purchase_date'].dtype == 'object':
        features['last_purchase_date'] = pd.to_datetime(features['last_purchase_date'])
    
    # Create spending categories
    features['spending_level'] = pd.cut(
        features['total_spent'],
        bins=[0, 100, 500, 1000, 10000],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    
    # Create order frequency categories
    features['order_frequency'] = pd.cut(
        features['total_orders'],
        bins=[0, 2, 5, 10, 1000],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    
    # Create purchase recency categories
    features['purchase_recency'] = pd.cut(
        features['last_purchase_days'],
        bins=[0, 7, 30, 90, 1000],
        labels=['Very Recent', 'Recent', 'Moderate', 'Inactive']
    )
    
    # Create payment method encoding
    payment_mapping = {
        'Credit Card': 1, 'Debit Card': 2, 'PayPal': 3, 'Apple Pay': 4, 'Google Pay': 5
    }
    features['payment_method_encoded'] = features['favorite_payment_method'].map(payment_mapping)
    
    # Calculate customer lifetime value (CLV) approximation
    features['clv_estimate'] = features['total_spent'] * (1 + features['total_orders'] * 0.1)
    
    # Create customer value categories
    features['customer_value'] = pd.cut(
        features['clv_estimate'],
        bins=[0, 200, 1000, 5000, 100000],
        labels=['Bronze', 'Silver', 'Gold', 'Platinum']
    )
    
    # Select final features for feature store
    final_features = features[[
        'user_id', 'total_spent', 'avg_order_value', 'total_orders',
        'last_purchase_days', 'favorite_payment_method', 'event_timestamp'
    ]].copy()
    
    print(f"✅ Engineered {len(final_features)} transaction features")
    return final_features


def engineer_product_features(products_df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer product features
    
    Args:
        products_df: Raw product data DataFrame
    
    Returns:
        DataFrame with engineered product features
    """
    print("🔧 Engineering product features...")
    
    # Create a copy to avoid modifying original data
    features = products_df.copy()
    
    # Create price categories
    features['price_category'] = pd.cut(
        features['price'],
        bins=[0, 20, 50, 100, 1000],
        labels=['Budget', 'Mid-range', 'Premium', 'Luxury']
    )
    
    # Create rating categories
    features['rating_category'] = pd.cut(
        features['avg_rating'],
        bins=[0, 3, 4, 4.5, 5],
        labels=['Poor', 'Good', 'Very Good', 'Excellent']
    )
    
    # Create review volume categories
    features['review_volume'] = pd.cut(
        features['total_reviews'],
        bins=[0, 10, 50, 200, 10000],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    
    # Create inventory status
    features['inventory_status'] = pd.cut(
        features['inventory_level'],
        bins=[0, 10, 50, 200, 10000],
        labels=['Low Stock', 'Medium Stock', 'High Stock', 'Overstocked']
    )
    
    # Create category encoding
    category_mapping = {
        'Electronics': 1, 'Clothing': 2, 'Books': 3, 'Home': 4, 'Sports': 5,
        'Beauty': 6, 'Toys': 7, 'Automotive': 8, 'Health': 9, 'Garden': 10
    }
    features['category_encoded'] = features['category'].map(category_mapping)
    
    # Calculate popularity score
    features['popularity_score'] = (
        features['avg_rating'] * 0.4 +
        np.log1p(features['total_reviews']) * 0.3 +
        (1 / (1 + features['price'] / 100)) * 0.3
    )
    
    # Create popularity categories
    features['popularity_level'] = pd.cut(
        features['popularity_score'],
        bins=[0, 2, 3, 4, 5],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    
    # Select final features for feature store
    final_features = features[[
        'product_id', 'category', 'price', 'avg_rating', 'total_reviews',
        'inventory_level', 'event_timestamp'
    ]].copy()
    
    print(f"✅ Engineered {len(final_features)} product features")
    return final_features


def engineer_all_features(raw_data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Engineer all features from raw data
    
    Args:
        raw_data: Dictionary containing raw data DataFrames
    
    Returns:
        Dictionary containing engineered feature DataFrames
    """
    print("🚀 Starting feature engineering pipeline...")
    
    engineered_features = {}
    
    # Engineer user demographic features
    if 'users' in raw_data:
        engineered_features['user_demographic'] = engineer_user_demographic_features(raw_data['users'])
    
    # Engineer user behavior features
    if 'behavior' in raw_data:
        engineered_features['user_behavior'] = engineer_user_behavior_features(raw_data['behavior'])
    
    # Engineer transaction features
    if 'transactions' in raw_data:
        engineered_features['transaction'] = engineer_transaction_features(raw_data['transactions'])
    
    # Engineer product features
    if 'products' in raw_data:
        engineered_features['product'] = engineer_product_features(raw_data['products'])
    
    print("✅ Feature engineering pipeline completed!")
    
    return engineered_features


def engineer_all_features_for_demo(raw_data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Engineer all features for demo purposes (shows all derived features)
    Args:
        raw_data: Dictionary containing raw data DataFrames
    Returns:
        Dictionary containing all engineered feature DataFrames (including derived features)
    """
    print("🚀 Starting feature engineering pipeline for demo...")
    engineered_features = {}
    # User Demographic
    if 'users' in raw_data:
        features = raw_data['users'].copy()
        if features['registration_date'].dtype == 'object':
            features['registration_date'] = pd.to_datetime(features['registration_date'])
        features['user_tenure_days'] = (datetime.now() - features['registration_date']).dt.days
        features['age_group'] = pd.cut(features['age'], bins=[0, 25, 35, 45, 55, 100], labels=['18-25', '26-35', '36-45', '46-55', '55+'])
        major_cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
        features['is_major_city'] = features['location'].isin(major_cities)
        features['gender_encoded'] = features['gender'].map({'M': 1, 'F': 2, 'Other': 3})
        features['registration_month'] = features['registration_date'].dt.month
        features['registration_day_of_week'] = features['registration_date'].dt.dayofweek
        features['is_premium'] = features['is_premium'].astype(int)
        engineered_features['user_demographic'] = features.copy()
    # User Behavior
    if 'behavior' in raw_data:
        features = raw_data['behavior'].copy()
        features['session_frequency'] = pd.cut(features['total_sessions'], bins=[0, 5, 15, 30, 1000], labels=['Low', 'Medium', 'High', 'Very High'])
        features['session_duration_category'] = pd.cut(features['avg_session_duration'], bins=[0, 15, 30, 60, 1000], labels=['Short', 'Medium', 'Long', 'Very Long'])
        features['engagement_level'] = pd.cut(features['engagement_score'], bins=[0, 25, 50, 75, 100], labels=['Low', 'Medium', 'High', 'Very High'])
        features['activity_recency'] = pd.cut(features['last_login_days'], bins=[0, 1, 7, 30, 1000], labels=['Very Recent', 'Recent', 'Moderate', 'Inactive'])
        category_mapping = {'Electronics': 1, 'Clothing': 2, 'Books': 3, 'Home': 4, 'Sports': 5}
        features['favorite_category_encoded'] = features['favorite_category'].map(category_mapping)
        engineered_features['user_behavior'] = features.copy()
    # Transaction
    if 'transactions' in raw_data:
        features = raw_data['transactions'].copy()
        features['spending_level'] = pd.cut(features['total_spent'], bins=[0, 100, 500, 1000, 10000], labels=['Low', 'Medium', 'High', 'Very High'])
        features['order_frequency'] = pd.cut(features['total_orders'], bins=[0, 2, 5, 10, 1000], labels=['Low', 'Medium', 'High', 'Very High'])
        features['purchase_recency'] = pd.cut(features['last_purchase_days'], bins=[0, 7, 30, 90, 1000], labels=['Very Recent', 'Recent', 'Moderate', 'Inactive'])
        payment_mapping = {'Credit Card': 1, 'Debit Card': 2, 'PayPal': 3, 'Apple Pay': 4, 'Google Pay': 5}
        features['payment_method_encoded'] = features['favorite_payment_method'].map(payment_mapping)
        features['clv_estimate'] = features['total_spent'] * (1 + features['total_orders'] * 0.1)
        features['customer_value'] = pd.cut(features['clv_estimate'], bins=[0, 200, 1000, 5000, 100000], labels=['Bronze', 'Silver', 'Gold', 'Platinum'])
        engineered_features['transaction'] = features.copy()
    # Product
    if 'products' in raw_data:
        features = raw_data['products'].copy()
        features['price_category'] = pd.cut(features['price'], bins=[0, 20, 50, 100, 1000], labels=['Budget', 'Mid-range', 'Premium', 'Luxury'])
        features['rating_category'] = pd.cut(features['avg_rating'], bins=[0, 3, 4, 4.5, 5], labels=['Poor', 'Good', 'Very Good', 'Excellent'])
        features['review_volume'] = pd.cut(features['total_reviews'], bins=[0, 10, 50, 200, 10000], labels=['Low', 'Medium', 'High', 'Very High'])
        features['inventory_status'] = pd.cut(features['inventory_level'], bins=[0, 10, 50, 200, 10000], labels=['Low Stock', 'Medium Stock', 'High Stock', 'Overstocked'])
        category_mapping = {'Electronics': 1, 'Clothing': 2, 'Books': 3, 'Home': 4, 'Sports': 5, 'Beauty': 6, 'Toys': 7, 'Automotive': 8, 'Health': 9, 'Garden': 10}
        features['category_encoded'] = features['category'].map(category_mapping)
        features['popularity_score'] = (features['avg_rating'] * 0.4 + np.log1p(features['total_reviews']) * 0.3 + (1 / (1 + features['price'] / 100)) * 0.3)
        features['popularity_level'] = pd.cut(features['popularity_score'], bins=[0, 2, 3, 4, 5], labels=['Low', 'Medium', 'High', 'Very High'])
        engineered_features['product'] = features.copy()
    print("✅ Feature engineering pipeline for demo completed!")
    return engineered_features


def validate_engineered_features(engineered_features: Dict[str, pd.DataFrame]) -> bool:
    """
    Validate engineered features quality
    
    Args:
        engineered_features: Dictionary containing engineered feature DataFrames
    
    Returns:
        bool: True if features are valid, False otherwise
    """
    try:
        for name, df in engineered_features.items():
            print(f"📋 Validating {name} features:")
            print(f"  - Shape: {df.shape}")
            print(f"  - Missing values: {df.isnull().sum().sum()}")
            print(f"  - Duplicates: {df.duplicated().sum()}")
            
            # Check for required columns
            required_cols = ['event_timestamp']
            if 'user_id' in df.columns:
                required_cols.append('user_id')
            elif 'product_id' in df.columns:
                required_cols.append('product_id')
            
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                print(f"❌ Missing required columns: {missing_cols}")
                return False
            
            if df.isnull().sum().sum() > 0:
                print(f"⚠️ Warning: {name} has missing values")
            
            if df.duplicated().sum() > 0:
                print(f"⚠️ Warning: {name} has duplicate rows")
        
        return True
        
    except Exception as e:
        print(f"❌ Feature validation failed: {e}")
        return False 