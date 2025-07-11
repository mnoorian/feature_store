# Transaction Data Feature Engineering Project

A modular Python project for generating synthetic transaction data and creating 12-month rolling features for customer analysis.

## 📁 Project Structure

```
fs_poc_2/
├── src/                          # Core Python modules
│   ├── __init__.py
│   ├── data_generation.py        # Synthetic data generation
│   ├── feature_engineering.py    # 12-month rolling features
│   └── utils.py                  # Utilities (loading, analysis, viz)
├── scripts/                      # CLI scripts
│   ├── generate_data.py          # Generate synthetic data
│   └── generate_features.py      # Generate features
├── notebooks/                    # Jupyter notebooks for exploration
├── data/                         # Data files
│   ├── raw/                      # Raw data files
│   └── transformed/              # Processed/transformed data
├── output/                       # Generated outputs
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create and activate virtual environment
python3.10 -m venv venv_py310
source venv_py310/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Generate Synthetic Data

```bash
# Generate 100 customers and 1000 transactions
python scripts/generate_data.py
```

This creates:
- `data/raw/customers.csv` - Customer information
- `data/raw/transactions.csv` - Transaction data

### 3. Generate 12-Month Rolling Features

```bash
# Generate features and analysis
python scripts/generate_features.py
```

This creates:
- `data/transformed/customer_features_12months.csv` - All features for each customer
- `data/transformed/customer_segments_analysis.csv` - Segmentation analysis

## 📊 Features Generated

### Transaction Count Features
- `total_transactions_12m` - Total transactions in last 12 months
- `avg_transactions_per_month` - Average transactions per month

### Amount Features
- `total_amount_12m` - Total amount spent in last 12 months
- `avg_amount_12m` - Average transaction amount
- `max_amount_12m` / `min_amount_12m` - Min/max transaction amounts
- `std_amount_12m` - Standard deviation of amounts

### Transaction Type Features
- `purchase_count_12m` / `purchase_amount_12m`
- `withdrawal_count_12m` / `withdrawal_amount_12m`
- `transfer_count_12m` / `transfer_amount_12m`
- `deposit_count_12m` / `deposit_amount_12m`

### Behavioral Features
- `high_value_transactions_12m` - Count of high-value transactions
- `low_value_transactions_12m` - Count of low-value transactions
- `days_since_first_transaction` - Customer tenure

## 🏷️ Customer Segmentation

Customers are automatically segmented into:
- **High-Value Active**: >$10K total amount AND >20 transactions
- **Active**: >$5K total amount OR >10 transactions
- **High-Value Occasional**: Average amount >$500
- **Regular**: >5 transactions
- **Occasional**: Low activity customers
- **Inactive**: No transactions in 12 months

## 🔧 Using the Modules

### Generate Data Programmatically

```python
from src.data_generation import generate_synthetic_data

# Generate custom dataset
customers_df, transactions_df = generate_synthetic_data(
    num_customers=200,
    num_transactions=2000,
    output_dir='data/raw'
)
```

### Generate Features Programmatically

```python
from src.feature_engineering import generate_12month_features, segment_customers
from src.utils import load_data, analyze_features

# Load data
customers_df, transactions_df = load_data()

# Generate features
features_df = generate_12month_features(transactions_df)

# Add segmentation
features_df['customer_segment'] = segment_customers(features_df)

# Analyze
segment_analysis = analyze_features(features_df)
```

## 📈 Analysis & Visualization

The feature generation script automatically:
- Calculates descriptive statistics
- Creates customer segments
- Generates visualizations (histograms, scatter plots, pie charts)
- Exports results to CSV

## 🛠️ Development

### Adding New Features

1. Add feature calculation logic to `src/feature_engineering.py`
2. Update the `generate_12month_features()` function
3. Test with `python scripts/generate_features.py`

### Adding New Analysis

1. Add analysis functions to `src/utils.py`
2. Import and use in `scripts/generate_features.py`
3. Update visualizations as needed

## 📋 Requirements

- Python 3.10+
- pandas
- numpy
- matplotlib
- seaborn

## 📝 License

This project is for educational and demonstration purposes. 