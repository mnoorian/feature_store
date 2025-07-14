# Feast + DataHub Integration

A proof-of-concept project demonstrating the integration between [Feast](https://feast.dev/) (Feature Store) and [DataHub](https://datahubproject.io/) (Metadata Platform) using Docker Compose.

## 🎯 Overview

This project sets up a complete environment where you can:
- **Register features** in Feast (offline feature store)
- **Discover features** through the DataHub UI
- **Manage metadata** for your ML features

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Feast         │    │   DataHub       │    │   Infrastructure│
│   (Jupyter)     │    │   (UI + GMS)    │    │   (Docker)      │
│                 │    │                 │    │                 │
│ • Feature       │    │ • Feature       │    │ • MySQL         │
│   Registration  │    │   Discovery     │    │ • Elasticsearch │
│ • Offline Store │    │ • Metadata      │    │ • Kafka         │
│ • Jupyter       │    │   Management    │    │ • Zookeeper     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd fs_poc_2
```

### 2. Start Services

```bash
docker compose up -d
```

### 3. Access the Services

- **DataHub UI:** http://localhost:9002
- **Jupyter Notebook:** http://localhost:8888
- **DataHub API:** http://localhost:8080

## 📁 Project Structure

```
fs_poc_2/
├── docker-compose.yml      # Main service orchestration
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
├── src/                   # Source code
│   ├── __init__.py
│   ├── data_generation.py
│   ├── feature_engineering.py
│   └── utils.py
├── notebooks/             # Jupyter notebooks
├── data/                  # Data files
│   ├── raw/
│   └── transformed/
├── scripts/               # Utility scripts
│   ├── generate_data.py
│   └── generate_features.py
└── output/                # Generated outputs
```

## 🔧 Services

### Core Services

| Service | Port | Description |
|---------|------|-------------|
| DataHub Frontend | 9002 | Web UI for metadata discovery |
| DataHub GMS | 8080 | Backend API service |
| Jupyter Notebook | 8888 | Feast feature development |
| MySQL | 3307 | DataHub metadata storage |
| Elasticsearch | 9201 | Search and indexing |
| Kafka | 9093 | Event streaming |
| Schema Registry | 8081 | Schema management |
| Zookeeper | 2182 | Kafka coordination |

### Configuration

- **Authentication:** Disabled (no login required)
- **Data Persistence:** Docker volumes for MySQL, Elasticsearch, and Kafka
- **Network:** Custom Docker network for service communication

## 📊 Usage

### 1. Register Features in Feast

1. Open Jupyter: http://localhost:8888
2. Create a new notebook
3. Install Feast and register your features:

```python
import feast
from feast import FeatureStore

# Initialize feature store
store = FeatureStore(repo_path=".")

# Define and register features
# ... your feature definitions
```

### 2. Discover Features in DataHub

1. Open DataHub UI: http://localhost:9002
2. Search for your registered features
3. Browse metadata and lineage

### 3. Ingest Feast Metadata to DataHub

```bash
# Install DataHub CLI
pip install 'acryl-datahub[datahub-rest]'

# Ingest Feast metadata
datahub ingest -c feast-ingestion.yml
```

## 🛠️ Development

### Adding New Features

1. **Define features** in Jupyter notebooks
2. **Register** them in Feast
3. **Ingest metadata** into DataHub
4. **Discover** through DataHub UI

### Customizing the Setup

- Modify `docker-compose.yml` for different configurations
- Update `requirements.txt` for additional dependencies
- Add custom notebooks in the `notebooks/` directory

## 🔍 Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Check what's using a port
   lsof -i :<port>
   
   # Stop conflicting containers
   docker stop <container-name>
   ```

2. **Service Health Issues**
   ```bash
   # Check service status
   docker compose ps
   
   # View logs
   docker compose logs <service-name>
   ```

3. **Volume Issues**
   ```bash
   # Clean up volumes
   docker compose down
   docker volume rm <volume-name>
   docker compose up -d
   ```

### Service Logs

```bash
# View all logs
docker compose logs

# View specific service logs
docker compose logs datahub-gms
docker compose logs feast-jupyter
```

## 📝 Notes

- **Offline Features Only:** This setup focuses on offline feature stores (no Redis)
- **Development Environment:** Not recommended for production use
- **Data Persistence:** Data is stored in Docker volumes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

[Add your license here]

## 🙏 Acknowledgments

- [Feast](https://feast.dev/) - Feature Store
- [DataHub](https://datahubproject.io/) - Metadata Platform
- [Docker](https://www.docker.com/) - Containerization 