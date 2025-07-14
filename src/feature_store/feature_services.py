"""
Feature Service Definitions for Feast Feature Store

This module contains all feature service definitions that group related features
for easier consumption by ML models.
"""

from feast import FeatureService

from .feature_views import (
    get_user_demographic_features, get_user_behavior_features,
    get_transaction_features, get_product_features
)


def get_user_feature_service() -> FeatureService:
    """Get comprehensive user feature service"""
    return FeatureService(
        name="user_feature_service",
        features=[
            get_user_demographic_features(),
            get_user_behavior_features(),
            get_transaction_features()
        ],
        description="""
        Comprehensive user feature service combining demographic, behavior, and transaction features.
        
        **Use Cases:** User profiling, personalized recommendations, customer segmentation
        **Model Applications:** Churn prediction, CLV modeling, recommendation systems
        **Documentation:** https://github.com/your-org/feature-pipeline/wiki/user-features
        **Feature Count:** 3 feature views with 15 total features
        """
    )


def get_product_feature_service() -> FeatureService:
    """Get product feature service"""
    return FeatureService(
        name="product_feature_service",
        features=[get_product_features()],
        description="""
        Product feature service for product-related ML models.
        
        **Use Cases:** Product recommendations, inventory optimization, pricing strategies
        **Model Applications:** Product ranking, demand forecasting, price optimization
        **Documentation:** https://github.com/your-org/feature-pipeline/wiki/product-features
        **Feature Count:** 1 feature view with 5 total features
        """
    )


def get_behavior_feature_service() -> FeatureService:
    """Get user behavior feature service"""
    return FeatureService(
        name="behavior_feature_service",
        features=[
            get_user_behavior_features(),
            get_transaction_features()
        ],
        description="""
        User behavior and transaction feature service for engagement and purchase prediction.
        
        **Use Cases:** Engagement prediction, purchase behavior analysis, churn prevention
        **Model Applications:** Engagement scoring, purchase prediction, churn modeling
        **Documentation:** https://github.com/your-org/feature-pipeline/wiki/behavior-features
        **Feature Count:** 2 feature views with 10 total features
        """
    )


def get_all_feature_services():
    """Get all feature service definitions"""
    return [
        get_user_feature_service(),
        get_product_feature_service(),
        get_behavior_feature_service()
    ] 