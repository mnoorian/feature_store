# DataHub Integration with Feast Feature Store

This document explains how to integrate your Feast feature store with DataHub for enhanced metadata management and data lineage.

## Overview

DataHub is a metadata platform that helps you discover, understand, and trust your data. By integrating Feast with DataHub, you can:

- **Discover features**: Find and understand your ML features across the organization
- **Track lineage**: See how features are derived from source data
- **Monitor quality**: Track feature quality and freshness
- **Collaborate**: Share feature documentation and usage patterns

## Prerequisites

1. **DataHub instance running**: You need a DataHub instance accessible at `http://localhost:9002` (UI) and `http://localhost:8080` (API)
2. **Feast project initialized**: Your Feast project should be set up with entities and feature views
3. **Python dependencies**: Ensure DataHub is installed in your environment

## Installation

The DataHub integration is already included in your `requirements.txt`:

```bash
pip install acryl-datahub[datahub-rest]
```

## Quick Start

### Method 1: Using Python Module (Recommended)

```bash
# Make sure you're in the project root
cd /path/to/fs_poc_2

# Activate the feast environment
conda activate feast-env

# Run DataHub ingestion using Python module
python src/datahub_integration/ingestion.py
```

### Method 2: Using DataHub CLI Directly

```bash
# Make sure you're in the project root
cd /path/to/fs_poc_2

# Activate the feast environment
conda activate feast-env

# Run DataHub ingestion using CLI
datahub ingest -c configs/datahub_config.yaml
```

## Configuration

### DataHub Pipeline Configuration

The DataHub pipeline is configured in `configs/datahub_config.yaml`:

```yaml
source:
  type: feast
  config:
    project_name: fs_poc_2
    repo_path: ./
    registry_type: sqlite
    registry_path: ./data/registry.db
    provider: local

sink:
  type: datahub-rest
  config:
    server: http://localhost:8080
    token: ${DATAHUB_TOKEN}  # Optional: for authentication
    timeout_sec: 30
```

### Environment Variables

- `DATAHUB_TOKEN`: Optional authentication token for DataHub
- Set this if your DataHub instance requires authentication

### Customizing the Configuration

You can modify the configuration to:

1. **Change DataHub server URL**: Update the `server` field in the sink config
2. **Add authentication**: Set the `DATAHUB_TOKEN` environment variable
3. **Modify timeout**: Adjust the `timeout_sec` value
4. **Add transformers**: Uncomment and configure transformers in the config file

## What Gets Ingested

The DataHub integration ingests the following Feast metadata:

### Entities
- Entity definitions and their properties
- Primary keys and join keys
- Entity descriptions and tags

### Feature Views
- Feature view definitions
- Feature names and types
- Data sources and transformations
- TTL (Time To Live) settings

### Data Sources
- Source table definitions
- Schema information
- Data freshness metadata

### Feature Services
- Feature service definitions
- Feature references
- Service configurations

## Verification

After running the ingestion, you can verify the integration:

1. **Check DataHub UI**: Visit `http://localhost:9002` and search for your Feast entities
2. **Verify entities**: Look for entities like `user`, `transaction`, etc.
3. **Check feature views**: Search for feature views and their associated features
4. **Review lineage**: Navigate to the lineage tab to see data flow

## Troubleshooting

### Common Issues

1. **DataHub not running**
   ```
   Error: Connection refused
   ```
   **Solution**: Start your DataHub instance first

2. **Registry not found**
   ```
   Error: Registry database not found
   ```
   **Solution**: Run Feast commands to initialize the registry first

3. **Authentication required**
   ```
   Error: 401 Unauthorized
   ```
   **Solution**: Set the `DATAHUB_TOKEN` environment variable

4. **Import errors**
   ```
   ImportError: No module named 'datahub'
   ```
   **Solution**: Install DataHub: `pip install acryl-datahub[datahub-rest]`

### Debug Mode

To run with debug logging:

```bash
# Set debug environment variable
export DATAHUB_DEBUG=1

# Run the ingestion
python src/datahub_integration/ingestion.py
```

## Advanced Usage

### Custom Transformers

You can add custom transformers to modify metadata during ingestion:

```yaml
transformers:
  - type: "datahub.ingestion.transformer.add_dataset_browse_path"
    config:
      path_elements: ["feast", "features"]
```

### Scheduled Ingestion

To run ingestion automatically, you can:

1. **Use cron** (Linux/Mac):
   ```bash
   # Add to crontab - run every hour
   0 * * * * cd /path/to/fs_poc_2 && conda activate feast-env && python src/datahub_integration/ingestion.py
   ```

2. **Use systemd** (Linux):
   Create a systemd service file for automated ingestion

3. **Use CI/CD**: Add the ingestion step to your CI/CD pipeline

### Monitoring

Monitor the ingestion process by:

1. **Checking logs**: The script provides colored output for status tracking
2. **DataHub metrics**: Use DataHub's built-in metrics and monitoring
3. **Custom alerts**: Set up alerts for failed ingestion runs

## Best Practices

1. **Regular ingestion**: Run ingestion after significant changes to your feature store
2. **Version control**: Keep your DataHub config in version control
3. **Testing**: Test ingestion in a staging environment first
4. **Documentation**: Keep feature documentation up to date in DataHub
5. **Access control**: Use DataHub's access control features to manage permissions

## Next Steps

After successful integration:

1. **Explore the UI**: Familiarize yourself with DataHub's interface
2. **Add documentation**: Enhance feature descriptions and tags
3. **Set up alerts**: Configure monitoring for data quality issues
4. **Train your team**: Help others understand how to use DataHub for feature discovery

## Support

For issues with:

- **DataHub integration**: Check the troubleshooting section above
- **Feast configuration**: Refer to the Feast documentation
- **DataHub platform**: Visit the [DataHub documentation](https://datahubproject.io/docs)

## Files Created

- `configs/datahub_config.yaml`: Configuration file for DataHub pipeline
- `src/datahub_integration/ingestion.py`: Python module for running DataHub ingestion
- `docs/datahub_integration.md`: This documentation file 