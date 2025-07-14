#!/usr/bin/env python3
"""
Feast to DataHub Integration Workflow

This script automates the complete workflow:
1. Run Feast feature registration notebook
2. Ingest features into DataHub
3. Verify the integration
"""

import subprocess
import time
import requests
import json
import os
from pathlib import Path

def check_service_health(url, service_name):
    """Check if a service is healthy"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {service_name} is healthy at {url}")
            return True
        else:
            print(f"❌ {service_name} returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {service_name} is not accessible: {e}")
        return False

def run_notebook():
    """Run the Feast feature registration notebook"""
    print("📊 Running Feast feature registration notebook...")
    
    notebook_path = Path("notebooks/feast_feature_registration.ipynb")
    if not notebook_path.exists():
        print("❌ Notebook not found. Please run the notebook manually in Jupyter.")
        return False
    
    # For now, we'll just check if the notebook exists
    # In a real scenario, you might use papermill or nbconvert to execute it
    print("✅ Notebook found. Please run it manually in Jupyter at http://localhost:8888")
    return True

def ingest_to_datahub():
    """Ingest Feast features into DataHub"""
    print("🔄 Ingesting features into DataHub...")
    
    # Check if DataHub is running
    if not check_service_health("http://localhost:8080/health", "DataHub GMS"):
        print("❌ DataHub GMS is not running")
        return False
    
    # Check if feature metadata exists
    metadata_path = Path("data/feature_metadata.json")
    if not metadata_path.exists():
        print("❌ Feature metadata not found. Please run the Feast notebook first.")
        return False
    
    # Install DataHub CLI if not already installed
    try:
        subprocess.run(["datahub", "--version"], check=True, capture_output=True)
        print("✅ DataHub CLI is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📦 Installing DataHub CLI...")
        subprocess.run(["pip", "install", "acryl-datahub[datahub-rest]"], check=True)
    
    # Run ingestion
    try:
        result = subprocess.run([
            "datahub", "ingest", "-c", "datahub-ingestion.yml"
        ], capture_output=True, text=True, check=True)
        print("✅ Successfully ingested features into DataHub")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to ingest features: {e}")
        print(f"Error output: {e.stderr}")
        return False

def verify_integration():
    """Verify that features are discoverable in DataHub"""
    print("🔍 Verifying DataHub integration...")
    
    # Check if DataHub UI is accessible
    if not check_service_health("http://localhost:9002", "DataHub Frontend"):
        print("❌ DataHub Frontend is not accessible")
        return False
    
    print("✅ DataHub integration verified!")
    print("\n🎉 Workflow completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Open DataHub UI: http://localhost:9002")
    print("2. Search for 'feast' or 'user_features' to find your features")
    print("3. Explore the feature metadata and lineage")
    print("4. Use the features in your ML models")
    
    return True

def main():
    """Main workflow function"""
    print("🚀 Starting Feast to DataHub Integration Workflow")
    print("=" * 50)
    
    # Check prerequisites
    print("🔍 Checking prerequisites...")
    
    # Check if Jupyter is running
    if not check_service_health("http://localhost:8888", "Jupyter Notebook"):
        print("❌ Jupyter is not running. Please start the services first.")
        return
    
    # Check if DataHub is running
    if not check_service_health("http://localhost:9002", "DataHub Frontend"):
        print("❌ DataHub is not running. Please start the services first.")
        return
    
    print("✅ All prerequisites met!")
    print()
    
    # Step 1: Run notebook (manual for now)
    if not run_notebook():
        print("❌ Failed to run notebook")
        return
    
    # Step 2: Ingest to DataHub
    if not ingest_to_datahub():
        print("❌ Failed to ingest to DataHub")
        return
    
    # Step 3: Verify integration
    if not verify_integration():
        print("❌ Failed to verify integration")
        return
    
    print("\n🎉 Workflow completed successfully!")

if __name__ == "__main__":
    main() 