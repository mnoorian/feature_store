"""
Feature View Definitions for Feast Feature Store

This module contains all feature view definitions with comprehensive metadata,
GitHub links to code logic, and business descriptions.
"""

from datetime import timedelta
from feast import FeatureView, Field
from feast.types import Float32, Int64, String, Bool

from .entities import get_user_entity, get_product_entity
from .data_sources import (
    get_user_demographic_source, get_user_behavior_source,
    get_transaction_source, get_product_source
)


def get_user_demographic_features() -> FeatureView:
    """Get user demographic feature view"""
    return FeatureView(
        name="user_demographic_features",
        entities=[get_user_entity()],
        ttl=timedelta(days=365),
        schema=[
            Field(name="age", dtype=Int64, description="User age in years"),
            Field(name="gender", dtype=String, description="User gender (M/F/Other)"),
            Field(name="location", dtype=String, description="User location/city"),
            Field(name="registration_date", dtype=String, description="User registration date"),
            Field(name="is_premium", dtype=Bool, description="Whether user has premium subscription")
        ],
        source=get_user_demographic_source(),
        description="""
        User demographic features from local CSV data.
        
        **Code Logic:** https://github.com/your-org/feature-pipeline/blob/main/src/features/user_demographics.py
        **Data Source:** Local CSV file: data/transformed/user_demographic_features.csv
        **Update Frequency:** Daily
        **Business Use Cases:** User segmentation, personalized recommendations, marketing campaigns
        **Feature Generation Script:** https://github.com/your-org/feature-pipeline/blob/main/scripts/generate_user_demographics.py
        """
    )


def get_user_behavior_features() -> FeatureView:
    """Get user behavior feature view"""
    return FeatureView(
        name="user_behavior_features",
        entities=[get_user_entity()],
        ttl=timedelta(days=90),
        schema=[
            Field(name="avg_session_duration", dtype=Float32, description="Average session duration in minutes"),
            Field(name="total_sessions", dtype=Int64, description="Total number of sessions in last 30 days"),
            Field(name="favorite_category", dtype=String, description="Most frequently viewed category"),
            Field(name="last_login_days", dtype=Int64, description="Days since last login"),
            Field(name="engagement_score", dtype=Float32, description="User engagement score (0-100)")
        ],
        source=get_user_behavior_source(),
        description="""
        User behavior features derived from session data and user interactions.
        
        **Code Logic:** https://github.com/your-org/feature-pipeline/blob/main/src/features/user_behavior.py
        **Data Source:** Local CSV file: data/transformed/user_behavior_features.csv
        **Update Frequency:** Hourly
        **Business Use Cases:** Churn prediction, engagement optimization, user experience improvements
        **Feature Generation Script:** https://github.com/your-org/feature-pipeline/blob/main/scripts/generate_user_behavior.py
        """
    )


def get_transaction_features() -> FeatureView:
    """Get transaction feature view"""
    return FeatureView(
        name="transaction_features",
        entities=[get_user_entity()],
        ttl=timedelta(days=365),
        schema=[
            Field(name="total_spent", dtype=Float32, description="Total amount spent by user"),
            Field(name="avg_order_value", dtype=Float32, description="Average order value"),
            Field(name="total_orders", dtype=Int64, description="Total number of orders"),
            Field(name="last_purchase_days", dtype=Int64, description="Days since last purchase"),
            Field(name="favorite_payment_method", dtype=String, description="Most used payment method")
        ],
        source=get_transaction_source(),
        description="""
        Transaction features derived from purchase history and payment data.
        
        **Code Logic:** https://github.com/your-org/feature-pipeline/blob/main/src/features/transaction_features.py
        **Data Source:** Local CSV file: data/transformed/transaction_features.csv
        **Update Frequency:** Real-time
        **Business Use Cases:** Customer lifetime value, purchase prediction, fraud detection
        **Feature Generation Script:** https://github.com/your-org/feature-pipeline/blob/main/scripts/generate_transaction_features.py
        """
    )


def get_product_features() -> FeatureView:
    """Get product feature view"""
    return FeatureView(
        name="product_features",
        entities=[get_product_entity()],
        ttl=timedelta(days=180),
        schema=[
            Field(name="category", dtype=String, description="Product category"),
            Field(name="price", dtype=Float32, description="Product price"),
            Field(name="avg_rating", dtype=Float32, description="Average product rating"),
            Field(name="total_reviews", dtype=Int64, description="Total number of reviews"),
            Field(name="inventory_level", dtype=Int64, description="Current inventory level")
        ],
        source=get_product_source(),
        description="""
        Product features including category, price, ratings, and inventory information.
        
        **Code Logic:** https://github.com/your-org/feature-pipeline/blob/main/src/features/product_features.py
        **Data Source:** Local CSV file: data/transformed/product_features.csv
        **Update Frequency:** Daily
        **Business Use Cases:** Product recommendations, inventory optimization, pricing strategies
        **Feature Generation Script:** https://github.com/your-org/feature-pipeline/blob/main/scripts/generate_product_features.py
        """
    )


def get_all_feature_views():
    """Get all feature view definitions"""
    return [
        get_user_demographic_features(),
        get_user_behavior_features(),
        get_transaction_features(),
        get_product_features()
    ] 