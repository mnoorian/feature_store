# 🔍 Feature Discovery Guide

This folder contains various methods to discover and explore features in your Feast feature store.

## 🚀 Quick Start

### Prerequisites
```bash
conda activate feast-env
cd /path/to/fs_poc_2
```

### Start Here
```bash
python feature_discovery/quick_start.py
```

## 📋 Available Methods

| Method | Script | Use Case |
|--------|--------|----------|
| **Quick Start** | `quick_start.py` | Get started immediately |
| **Method 1** | `method1_builtin.py` | Quick overview using built-in function |
| **Method 2** | `method2_cli.py` | Detailed CLI exploration |
| **Method 3** | `method3_interactive.py` | Custom Python with search |
| **Method 4** | `method4_metadata.py` | JSON metadata exploration |
| **Method 5** | `method5_datahub.py` | **DataHub integration discovery** |
| **All Methods** | `run_all_methods.py` | Run all methods sequentially |

## 🎯 Method Details

### Method 1: Built-in Function
```bash
python feature_discovery/method1_builtin.py
```
- Uses your existing `list_registered_features()` function
- Fast and simple overview
- Shows all registered features

### Method 2: Feast CLI
```bash
python feature_discovery/method2_cli.py
```
- Automated Feast CLI commands
- Structured table format
- Detailed feature descriptions

### Method 3: Interactive Python
```bash
python feature_discovery/method3_interactive.py
```
- Custom Python exploration
- Keyword search functionality
- Feature statistics

### Method 4: JSON Metadata
```bash
python feature_discovery/method4_metadata.py
```
- Uses exported JSON metadata
- Generates markdown report
- External integration ready

### Method 5: DataHub Integration
```bash
python feature_discovery/method5_datahub.py
```
- **Discovers features through DataHub**
- Compares Feast vs DataHub features
- Enterprise cataloging and lineage
- Real-time feature search

## 📊 Current Features

### 🔑 Entities (2)
- **user_id**: Unique identifier for users (INT64)
- **product_id**: Unique identifier for products (INT64)

### 📊 Feature Views (4)
1. **user_demographic_features** (6 features)
2. **user_behavior_features** (6 features)
3. **transaction_features** (6 features)
4. **product_features** (6 features)

### 🛠️ Feature Services (3)
1. **user_feature_service**: 15 features
2. **product_feature_service**: 5 features
3. **behavior_feature_service**: 10 features

## 🔧 Troubleshooting

### Environment Issues
```bash
# Check available environments
conda env list

# Activate feast-env
conda activate feast-env

# Verify Feast installation
python -c "import feast; print(feast.__version__)"
```

### Import Errors
```bash
# Make sure you're in project root
pwd  # Should show: /path/to/fs_poc_2

# Check if features are registered
ls -la data/registry.db
```

## 📝 Next Steps

After discovering features, you can:

1. **Get Historical Features** for training:
   ```python
   training_df = store.get_historical_features(entity_df, features)
   ```

2. **Get Online Features** for inference:
   ```python
   features = store.get_online_features(features, entity_rows)
   ```

3. **Explore DataHub Integration** for feature lineage and discovery

## 📖 Resources

- [Feast Documentation](https://docs.feast.dev/)
- [Feature Store Architecture](../README.md)
- [DataHub Integration Guide](../scripts/)
- [DataHub Discovery Method](./method5_datahub.py) 