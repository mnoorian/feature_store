"""
Entity Definitions for Feast Feature Store

This module contains all entity definitions used across the feature store.
Entities represent the primary keys for features.
"""

from feast import Entity, ValueType


def get_user_entity() -> Entity:
    """Get user entity definition"""
    return Entity(
        name="user_id",
        value_type=ValueType.INT64,
        description="Unique identifier for users. Used as primary key for user-related features.",
        join_keys=["user_id"]
    )


def get_product_entity() -> Entity:
    """Get product entity definition"""
    return Entity(
        name="product_id",
        value_type=ValueType.INT64,
        description="Unique identifier for products. Used as primary key for product-related features.",
        join_keys=["product_id"]
    )


def get_all_entities():
    """Get all entity definitions"""
    return [
        get_user_entity(),
        get_product_entity()
    ] 