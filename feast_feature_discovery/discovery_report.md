# Feature Discovery Report

Generated on: 2025-07-16T16:14:17.666949

## Overview

- **Feature Store**: feast_offline_store
- **Export Timestamp**: 2025-07-14T18:07:29.567019

## Summary Statistics

- **Entities**: 2
- **Feature Views**: 4
- **Feature Services**: 3

## Feature Views

### user_demographic_features
- **Entities**: user_id
- **Features**: is_premium, user_id, registration_date, location, gender, age
- **Source**: data/transformed/user_demographic_features.csv
- **TTL**: 365 days, 0:00:00

### user_behavior_features
- **Entities**: user_id
- **Features**: user_id, total_sessions, favorite_category, engagement_score, avg_session_duration, last_login_days
- **Source**: data/transformed/user_behavior_features.csv
- **TTL**: 90 days, 0:00:00

### transaction_features
- **Entities**: user_id
- **Features**: user_id, favorite_payment_method, total_spent, last_purchase_days, total_orders, avg_order_value
- **Source**: data/transformed/transaction_features.csv
- **TTL**: 365 days, 0:00:00

### product_features
- **Entities**: product_id
- **Features**: inventory_level, price, category, avg_rating, product_id, total_reviews
- **Source**: data/transformed/product_features.csv
- **TTL**: 180 days, 0:00:00

