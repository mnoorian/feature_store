"""
Data Source Definitions for Feast Feature Store

This module contains all data source definitions including local CSV files and S3 placeholders.
"""

from feast import FileSource


def get_user_demographic_source() -> FileSource:
    """Get user demographic data source"""
    return FileSource(
        name="user_demographic_source",
        path="data/transformed/user_demographic_features.csv",
        timestamp_field="event_timestamp",
        description="User demographic features from local CSV data. Contains age, gender, location, and subscription status."
    )


def get_user_behavior_source() -> FileSource:
    """Get user behavior data source"""
    return FileSource(
        name="user_behavior_source",
        path="data/transformed/user_behavior_features.csv",
        timestamp_field="event_timestamp",
        description="User behavior features from local CSV data. Contains session metrics and engagement scores."
    )


def get_transaction_source() -> FileSource:
    """Get transaction data source"""
    return FileSource(
        name="transaction_source",
        path="data/transformed/transaction_features.csv",
        timestamp_field="event_timestamp",
        description="Transaction features from local CSV data. Contains purchase history and payment information."
    )


def get_product_source() -> FileSource:
    """Get product data source"""
    return FileSource(
        name="product_source",
        path="data/transformed/product_features.csv",
        timestamp_field="event_timestamp",
        description="Product features from local CSV data. Contains product metadata and performance metrics."
    )


def get_s3_user_demographic_source() -> FileSource:
    """Get S3 placeholder for user demographic data source"""
    return FileSource(
        name="user_demographic_source",
        path="s3://your-bucket/features/user_demographic_features.parquet",
        timestamp_field="event_timestamp",
        description="User demographic features stored in S3. Contains age, gender, location, and subscription status."
    )


def get_s3_user_behavior_source() -> FileSource:
    """Get S3 placeholder for user behavior data source"""
    return FileSource(
        name="user_behavior_source",
        path="s3://your-bucket/features/user_behavior_features.parquet",
        timestamp_field="event_timestamp",
        description="User behavior features stored in S3. Contains session metrics and engagement scores."
    )


def get_s3_transaction_source() -> FileSource:
    """Get S3 placeholder for transaction data source"""
    return FileSource(
        name="transaction_source",
        path="s3://your-bucket/features/transaction_features.parquet",
        timestamp_field="event_timestamp",
        description="Transaction features stored in S3. Contains purchase history and payment information."
    )


def get_s3_product_source() -> FileSource:
    """Get S3 placeholder for product data source"""
    return FileSource(
        name="product_source",
        path="s3://your-bucket/features/product_features.parquet",
        timestamp_field="event_timestamp",
        description="Product features stored in S3. Contains product metadata and performance metrics."
    )


def get_all_local_sources():
    """Get all local CSV data sources"""
    return [
        get_user_demographic_source(),
        get_user_behavior_source(),
        get_transaction_source(),
        get_product_source()
    ]


def get_all_s3_sources():
    """Get all S3 placeholder data sources"""
    return [
        get_s3_user_demographic_source(),
        get_s3_user_behavior_source(),
        get_s3_transaction_source(),
        get_s3_product_source()
    ] 