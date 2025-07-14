# Feature Store POC with Feast and DataHub

A comprehensive feature store implementation using **Feast** for feature management and **DataHub** for feature discovery and lineage tracking. This project demonstrates a complete ML feature pipeline from data generation to feature serving.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Raw Data      │    │   Engineered    │    │   Feature Store │
│   Generation    │───▶│   Features      │───▶│   (Feast)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Local CSV     │    │   CSV Export    │    │   Metadata      │
│   Files         │    │   (Transformed) │    │   Export        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                              │
                                                              ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   DataHub       │◀───│   Metadata      │◀───│   Feature       │
│   UI/API        │    │   Ingestion     │    │   Discovery     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🔄 Metadata Flow

1. **Feature Registration**: Features are registered in Feast with metadata
2. **Metadata Export**: Feast metadata is exported to DataHub-compatible format
3. **DataHub Ingestion**: Metadata is ingested into DataHub via API/UI
4. **Feature Discovery**: Users can discover and explore features in DataHub UI

### 📊 Infrastructure Components

- **Feast**: Feature store for feature management and serving
- **DataHub**: Metadata catalog for feature discovery and lineage
- **Kafka**: Message streaming (for real-time features)
- **MySQL**: Metadata storage for DataHub
- **Elasticsearch**: Search and indexing for DataHub
- **Jupyter**: Development and experimentation environment

## 📁 Project Structure

```
fs_poc_2/
├── data/                          # Data storage
│   ├── raw/                       # Raw data files
│   ├── transformed/               # Engineered features
│   └── feature_metadata.json      # DataHub metadata
├── src/                           # Source code
│   ├── feature_store/             # Feast feature store definitions
│   │   ├── __init__.py
│   │   ├── entities.py            # Entity definitions
│   │   ├── data_sources.py        # Data source definitions
│   │   ├── feature_views.py       # Feature view definitions
│   │   ├── feature_services.py    # Feature service definitions
│   │   └── registry.py            # Registration and metadata export
│   ├── feature_generation/        # Feature engineering pipeline
│   │   ├── __init__.py
│   │   ├── data_loader.py         # Data loading and generation
│   │   ├── feature_engineering.py # Feature engineering logic
│   │   └── data_exporter.py       # Data export utilities
│   └── pipeline.py                # Main orchestration pipeline
├── scripts/                       # Utility scripts
│   ├── run_pipeline.py            # Pipeline runner script
│   ├── upload_features_direct.py  # Direct DataHub API upload
│   └── ingest_to_datahub.py       # DataHub metadata ingestion
├── notebooks/                     # Jupyter notebooks
│   └── feature_store_demo.ipynb   # Comprehensive demo notebook
├── docker-compose.yml             # Docker services configuration
├── feature_store.yaml             # Feast configuration
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- Docker and Docker Compose
- Python 3.8+
- Git

### 2. Clone and Setup

```bash
git clone <your-repo-url>
cd fs_poc_2

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start Services

```bash
# Start DataHub and Feast Jupyter
docker-compose up -d

# Wait for services to be ready (check with docker-compose ps)
```

### 4. Access Services

- **DataHub UI**: http://localhost:9002 (no login required)
- **Jupyter Notebook**: http://localhost:8888 (no token required)

### 5. Run the Pipeline

```bash
# Run complete pipeline
python scripts/run_pipeline.py

# Or run individual phases
python scripts/run_pipeline.py --generate-only
python scripts/run_pipeline.py --register-only
```

## 📊 Features Included

### User Features
- **Demographic**: Age, gender, location, registration date, premium status
- **Behavior**: Session duration, total sessions, favorite category, engagement score
- **Transaction**: Total spent, average order value, order count, payment method

### Product Features
- **Metadata**: Category, price, average rating, review count, inventory level

## 🔧 Code Structure

### Feature Store Module (`src/feature_store/`)

The feature store module contains all Feast-related definitions:

#### Entities (`entities.py`)
```python
def get_user_entity() -> Entity:
    return Entity(
        name="user_id",
        value_type=ValueType.INT64,
        description="Unique identifier for users",
        join_keys=["user_id"]
    )
```

#### Data Sources (`data_sources.py`)
```python
def get_user_demographic_source() -> FileSource:
    return FileSource(
        name="user_demographic_source",
        path="data/transformed/user_demographic_features.csv",
        timestamp_field="event_timestamp"
    )
```

#### Feature Views (`feature_views.py`)
```python
def get_user_demographic_features() -> FeatureView:
    return FeatureView(
        name="user_demographic_features",
        entities=[get_user_entity()],
        ttl=timedelta(days=365),
        schema=[...],
        source=get_user_demographic_source(),
        description="User demographic features with GitHub links..."
    )
```

#### Feature Services (`feature_services.py`)
```python
def get_user_feature_service() -> FeatureService:
    return FeatureService(
        name="user_feature_service",
        features=[
            get_user_demographic_features(),
            get_user_behavior_features(),
            get_transaction_features()
        ]
    )
```

### Feature Generation Module (`src/feature_generation/`)

The feature generation module handles data processing and feature engineering:

#### Data Loader (`data_loader.py`)
- Generates sample data for demonstration
- Loads existing data files if available
- Validates data quality

#### Feature Engineering (`feature_engineering.py`)
- Transforms raw data into ML-ready features
- Creates derived features and aggregations
- Handles data type conversions and encoding

#### Data Exporter (`data_exporter.py`)
- Exports engineered features to CSV files
- Creates feature summaries and documentation
- Validates exported files

### Pipeline Module (`src/pipeline.py`)

The main pipeline orchestrates the entire process:

```python
def run_complete_pipeline():
    # Phase 1: Feature Generation
    result = generate_all_features()
    
    # Phase 2: Feature Registration
    register_features_in_feast()
    
    # Phase 3: Metadata Export
    export_metadata()
```

### Metadata Export and Ingestion

The feature store includes automatic metadata export from Feast to DataHub:

#### Registry Module (`src/feature_store/registry.py`)
```python
def export_feast_metadata():
    """Export Feast metadata to DataHub-compatible format"""
    # Extract feature views, entities, and services
    # Convert to DataHub entity format
    # Generate metadata files for ingestion
```

#### DataHub Integration Scripts

**Direct API Upload** (`scripts/upload_features_direct.py`):
- Uploads feature metadata directly to DataHub API
- Handles authentication and error handling
- Provides status feedback

**CLI Ingestion** (`scripts/ingest_to_datahub.py`):
- Uses DataHub CLI for metadata ingestion
- Supports batch processing
- Configurable ingestion options

#### Metadata Files Generated

- `data/datahub_metadata.json`: Main metadata file for DataHub ingestion
- `data/simple_datahub_metadata.json`: Simplified format for UI upload
- `data/datahub_ingestion_config.yaml`: CLI configuration file

## 🎯 Usage Examples

### Complete Feature Store Workflow

```bash
# 1. Start infrastructure
docker-compose up -d

# 2. Run complete pipeline (generates data, registers features, exports metadata)
python scripts/run_pipeline.py

# 3. Upload metadata to DataHub
python scripts/upload_features_direct.py

# 4. Access DataHub UI to explore features
# Open http://localhost:9002 and search for "feast"
```

### Run Complete Pipeline

```bash
# Basic run
python scripts/run_pipeline.py

# With custom options
python scripts/run_pipeline.py \
    --data-dir /path/to/data \
    --use-s3 \
    --verbose
```

### Generate Features Only

```bash
python scripts/run_pipeline.py --generate-only
```

### Register Features Only

```bash
python scripts/run_pipeline.py --register-only
```

### Export and Ingest Metadata

```bash
# Export metadata from Feast
python scripts/run_pipeline.py --export-metadata-only

# Upload to DataHub via API
python scripts/upload_features_direct.py

# Or use DataHub CLI (if installed)
datahub ingest -c data/datahub_ingestion_config.yaml
```

### Manual DataHub Upload

1. **Export metadata**: Run the pipeline to generate metadata files
2. **Access DataHub UI**: Go to http://localhost:9002
3. **Upload metadata**: Use the ingestion interface to upload `data/datahub_metadata.json`
4. **Search features**: Look for your features in the DataHub catalog

### Use S3 Sources

```bash
python scripts/run_pipeline.py --use-s3
```

### Skip Optional Steps

```bash
python scripts/run_pipeline.py \
    --skip-raw-export \
    --skip-summary \
    --skip-validation \
    --skip-metadata
```

## 📓 Jupyter Notebook

The `notebooks/feature_store_demo.ipynb` provides a comprehensive demonstration:

1. **Data Generation**: Create sample datasets
2. **Feature Engineering**: Transform raw data into features
3. **Feature Registration**: Register features in Feast
4. **Metadata Export**: Export metadata for DataHub
5. **Feature Exploration**: Explore registered features
6. **Integration Examples**: Show DataHub integration

## 🔗 DataHub Integration

### Metadata Structure

The exported metadata includes:

```json
{
  "export_timestamp": "2024-01-01T12:00:00",
  "feature_store": "feast_offline_store",
  "entities": [...],
  "feature_views": [...],
  "feature_services": [...]
}
```

### Feature Lineage

Each feature view includes:
- **GitHub Links**: Links to feature generation code
- **Data Sources**: Information about source data
- **Update Frequency**: How often features are updated
- **Business Use Cases**: How features are used
- **Feature Generation Scripts**: Links to automation scripts

### DataHub Discovery

1. Open DataHub UI at http://localhost:9002
2. Navigate to "Data Assets" or "Search"
3. Search for "feast" or feature names
4. View feature lineage and metadata

## 🏪 Feature Store Usage

### Get Features for Inference

```python
from feast import FeatureStore

store = FeatureStore(repo_path=".")

# Get online features
features = store.get_online_features(
    features=[
        'user_demographic_features:age',
        'user_behavior_features:engagement_score',
        'transaction_features:total_spent'
    ],
    entity_rows=[{'user_id': 1}, {'user_id': 2}]
)
```

### Get Historical Features for Training

```python
import pandas as pd

# Create entity DataFrame
entity_df = pd.DataFrame({
    'user_id': [1, 2, 3],
    'event_timestamp': pd.to_datetime(['2024-01-01', '2024-01-01', '2024-01-01'])
})

# Get historical features
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=store.get_feature_service('user_feature_service')
).to_df()
```

## 🔧 Configuration

### Feast Configuration (`feature_store.yaml`)

```yaml
project: feast_offline_store
provider: local
online_store:
  type: sqlite
  path: data/online_store.db
offline_store:
  type: file
  path: data/offline_store
registry:
  type: sqlite
  path: data/registry.db
```

### Docker Services (`docker-compose.yml`)

- **DataHub GMS**: Metadata service
- **DataHub Frontend**: Web UI
- **Feast Jupyter**: Development environment
- **MySQL**: Metadata storage
- **Elasticsearch**: Search index
- **Kafka**: Event streaming (for future use)

## 🧪 Testing

### Run Tests

```bash
# Run feature generation tests
python -m pytest tests/test_feature_generation.py

# Run feature store tests
python -m pytest tests/test_feature_store.py

# Run integration tests
python -m pytest tests/test_integration.py
```

### Validate Pipeline

```bash
# Validate feature store
python -c "from src.feature_store.registry import validate_feature_store; validate_feature_store()"

# Check exported files
python -c "from src.feature_generation.data_exporter import validate_exported_files; validate_exported_files()"
```

## 📈 Monitoring and Observability

### Feature Quality Metrics

- Missing value rates
- Data freshness
- Feature drift detection
- Usage statistics

### Pipeline Monitoring

- Execution time tracking
- Error rate monitoring
- Data volume metrics
- Feature update frequency

## 🚀 Production Deployment

### Environment Variables

```bash
export FEAST_PROJECT_NAME=production_feature_store
export DATAHUB_GMS_HOST=your-datahub-host
export S3_BUCKET=your-feature-bucket
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
```

### CI/CD Pipeline

```yaml
# .github/workflows/feature-pipeline.yml
name: Feature Pipeline
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  push:
    branches: [main]

jobs:
  feature-generation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Feature Pipeline
        run: python scripts/run_pipeline.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Port Conflicts**: Check if ports 9002, 8888 are available
2. **Docker Issues**: Restart Docker and try again
3. **Import Errors**: Ensure virtual environment is activated
4. **Data Issues**: Check data directory permissions

### Getting Help

- Check the logs: `docker-compose logs`
- Validate setup: `python scripts/run_pipeline.py --dry-run`
- Review configuration files
- Check DataHub UI for errors

## 📚 Additional Resources

- [Feast Documentation](https://docs.feast.dev/)
- [DataHub Documentation](https://datahubproject.io/docs/)
- [Feature Store Best Practices](https://www.featurestore.org/)
- [MLOps with Feature Stores](https://www.mlops.community/)

---

**Happy Feature Engineering! 🎉** 