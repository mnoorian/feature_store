import pandas as pd


def filter_completed_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Filter only completed transactions for feature engineering."""
    return df[df['status'] == 'completed'].copy()


def generate_12month_features(transactions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate 12-month rolling features for each customer.
    """
    features_list = []
    customers = transactions_df['customer_id'].unique()
    for customer_id in customers:
        cust_tx = transactions_df[transactions_df['customer_id'] == customer_id]
        latest_date = cust_tx['transaction_date'].max()
        twelve_months_ago = latest_date - pd.DateOffset(months=12)
        recent_tx = cust_tx[cust_tx['transaction_date'] >= twelve_months_ago]
        amount_series = recent_tx['amount']
        is_empty = recent_tx.shape[0] == 0
        q90 = amount_series.quantile(0.9) if not is_empty else 0
        q10 = amount_series.quantile(0.1) if not is_empty else 0
        features = {
            'customer_id': customer_id,
            'latest_transaction_date': latest_date,
            'twelve_months_ago': twelve_months_ago,
            'total_transactions_12m': len(recent_tx),
            'avg_transactions_per_month': len(recent_tx) / 12,
            'total_amount_12m': amount_series.sum(),
            'avg_amount_12m': amount_series.mean(),
            'max_amount_12m': amount_series.max(),
            'min_amount_12m': amount_series.min(),
            'std_amount_12m': amount_series.std(),
            'purchase_count_12m': len(recent_tx[recent_tx['transaction_type'] == 'purchase']),
            'withdrawal_count_12m': len(recent_tx[recent_tx['transaction_type'] == 'withdrawal']),
            'transfer_count_12m': len(recent_tx[recent_tx['transaction_type'] == 'transfer']),
            'deposit_count_12m': len(recent_tx[recent_tx['transaction_type'] == 'deposit']),
            'purchase_amount_12m': recent_tx[recent_tx['transaction_type'] == 'purchase']['amount'].sum() if not recent_tx[recent_tx['transaction_type'] == 'purchase'].empty else 0,
            'withdrawal_amount_12m': recent_tx[recent_tx['transaction_type'] == 'withdrawal']['amount'].sum() if not recent_tx[recent_tx['transaction_type'] == 'withdrawal'].empty else 0,
            'transfer_amount_12m': recent_tx[recent_tx['transaction_type'] == 'transfer']['amount'].sum() if not recent_tx[recent_tx['transaction_type'] == 'transfer'].empty else 0,
            'deposit_amount_12m': recent_tx[recent_tx['transaction_type'] == 'deposit']['amount'].sum() if not recent_tx[recent_tx['transaction_type'] == 'deposit'].empty else 0,
            'days_since_first_transaction': (latest_date - cust_tx['transaction_date'].min()).days,
            'days_since_last_transaction': 0,
            'high_value_transactions_12m': len(amount_series[amount_series > q90]) if not is_empty else 0,
            'low_value_transactions_12m': len(amount_series[amount_series < q10]) if not is_empty else 0,
        }
        # Handle NaN
        for k, v in features.items():
            if pd.isna(v):
                features[k] = 0
        features_list.append(features)
    return pd.DataFrame(features_list)


def segment_customers(features_df: pd.DataFrame) -> pd.Series:
    """Segment customers based on their 12-month transaction behavior."""
    def _segment(row):
        if row['total_amount_12m'] == 0:
            return 'Inactive'
        elif row['total_amount_12m'] > 10000 and row['total_transactions_12m'] > 20:
            return 'High-Value Active'
        elif row['total_amount_12m'] > 5000 or row['total_transactions_12m'] > 10:
            return 'Active'
        elif row['avg_amount_12m'] > 500:
            return 'High-Value Occasional'
        elif row['total_transactions_12m'] > 5:
            return 'Regular'
        else:
            return 'Occasional'
    return features_df.apply(_segment, axis=1).astype(str) 