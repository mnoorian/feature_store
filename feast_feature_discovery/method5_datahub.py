#!/usr/bin/env python3
"""
Method 5: DataHub Integration Discovery

Explores features through DataHub integration for enhanced discovery.
Best for: Enterprise feature cataloging and lineage tracking.
"""

import json
import requests
import sys
from pathlib import Path
from datetime import datetime

# DataHub configuration
DATAHUB_GMS_URL = "http://localhost:8080"
DATAHUB_FRONTEND_URL = "http://localhost:9002"

def check_datahub_health():
    """Check if DataHub is running and healthy"""
    try:
        response = requests.get(f"{DATAHUB_GMS_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ DataHub is running and healthy")
            return True
        else:
            print(f"❌ DataHub health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to DataHub: {e}")
        print("💡 Start DataHub with: docker-compose up -d")
        return False

def search_datahub_features(search_term="feast"):
    """Search for features in DataHub"""
    print(f"🔍 Searching DataHub for '{search_term}'...")
    
    try:
        # Search API endpoint
        search_url = f"{DATAHUB_GMS_URL}/entities?action=search"
        search_payload = {
            "input": search_term,
            "entity": "dataset",
            "start": 0,
            "count": 50
        }
        
        response = requests.post(
            search_url,
            json=search_payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            results = response.json()
            return results.get("value", {}).get("entities", [])
        else:
            print(f"❌ Search failed: {response.status_code}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Search error: {e}")
        return []

def get_feature_details(entity_urn):
    """Get detailed information about a feature entity"""
    try:
        response = requests.get(
            f"{DATAHUB_GMS_URL}/entities/{entity_urn}",
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to get details for {entity_urn}: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting details: {e}")
        return None

def display_datahub_features(features):
    """Display features found in DataHub"""
    if not features:
        print("❌ No features found in DataHub")
        print("💡 Upload features first: python scripts/upload_features_direct.py")
        return
    
    print(f"\n📊 Found {len(features)} features in DataHub:")
    print("-" * 60)
    
    for i, feature in enumerate(features, 1):
        urn = feature.get("urn", "")
        name = feature.get("name", "Unknown")
        description = feature.get("description", "No description")
        
        print(f"\n{i}. {name}")
        print(f"   URN: {urn}")
        print(f"   Description: {description[:100]}...")
        
        # Get additional details
        details = get_feature_details(urn)
        if details:
            aspects = details.get("value", {}).get("aspects", [])
            for aspect in aspects:
                if "DatasetProperties" in str(aspect):
                    props = aspect.get("com.linkedin.pegasus2avro.dataset.DatasetProperties", {})
                    custom_props = props.get("customProperties", {})
                    if custom_props:
                        print(f"   Features: {custom_props.get('feature_count', 'Unknown')}")
                        print(f"   Entities: {custom_props.get('entities', 'Unknown')}")
                        print(f"   TTL: {custom_props.get('ttl', 'Unknown')}")

def compare_feast_datahub():
    """Compare features between Feast and DataHub"""
    print("\n🔄 Comparing Feast vs DataHub features...")
    print("-" * 60)
    
    # Load Feast metadata
    try:
        with open("data/feature_metadata.json", 'r') as f:
            feast_metadata = json.load(f)
    except FileNotFoundError:
        print("❌ Feast metadata not found")
        return
    
    feast_features = {fv['name'] for fv in feast_metadata.get('feature_views', [])}
    
    # Get DataHub features
    datahub_features = search_datahub_features("feast")
    datahub_names = {f.get('name', '') for f in datahub_features}
    
    print(f"📊 Comparison Results:")
    print(f"   Feast features: {len(feast_features)}")
    print(f"   DataHub features: {len(datahub_names)}")
    
    # Find differences
    feast_only = feast_features - datahub_names
    datahub_only = datahub_names - feast_features
    common = feast_features & datahub_names
    
    if feast_only:
        print(f"\n🔴 Only in Feast: {len(feast_only)}")
        for name in feast_only:
            print(f"   - {name}")
    
    if datahub_only:
        print(f"\n🔵 Only in DataHub: {len(datahub_only)}")
        for name in datahub_only:
            print(f"   - {name}")
    
    if common:
        print(f"\n✅ In both: {len(common)}")
        for name in common:
            print(f"   - {name}")

def export_datahub_report():
    """Export a comprehensive DataHub discovery report"""
    print("\n📝 Generating DataHub discovery report...")
    
    # Get all features
    features = search_datahub_features("feast")
    
    report_content = f"""# DataHub Feature Discovery Report

Generated on: {datetime.now().isoformat()}

## DataHub Status

- **DataHub URL**: {DATAHUB_FRONTEND_URL}
- **GMS URL**: {DATAHUB_GMS_URL}
- **Status**: {'Healthy' if check_datahub_health() else 'Unhealthy'}

## Feature Summary

- **Total Features Found**: {len(features)}

## Feature Details

"""
    
    for feature in features:
        name = feature.get("name", "Unknown")
        description = feature.get("description", "No description")
        urn = feature.get("urn", "")
        
        report_content += f"### {name}\n"
        report_content += f"- **URN**: {urn}\n"
        report_content += f"- **Description**: {description}\n"
        
        # Get additional details
        details = get_feature_details(urn)
        if details:
            aspects = details.get("value", {}).get("aspects", [])
            for aspect in aspects:
                if "DatasetProperties" in str(aspect):
                    props = aspect.get("com.linkedin.pegasus2avro.dataset.DatasetProperties", {})
                    custom_props = props.get("customProperties", {})
                    if custom_props:
                        report_content += f"- **Features**: {custom_props.get('feature_count', 'Unknown')}\n"
                        report_content += f"- **Entities**: {custom_props.get('entities', 'Unknown')}\n"
                        report_content += f"- **TTL**: {custom_props.get('ttl', 'Unknown')}\n"
        
        report_content += "\n"
    
    # Write report
    report_path = "feature_discovery/datahub_discovery_report.md"
    with open(report_path, 'w') as f:
        f.write(report_content)
    
    print(f"✅ DataHub report saved to: {report_path}")

def main():
    print("🔍 Method 5: DataHub Integration Discovery")
    print("=" * 60)
    
    # Check DataHub health
    if not check_datahub_health():
        print("\n💡 DataHub is not available. Try:")
        print("   1. Start DataHub: docker-compose up -d")
        print("   2. Upload features: python scripts/upload_features_direct.py")
        print("   3. Run this script again")
        return
    
    # Search for features
    features = search_datahub_features()
    display_datahub_features(features)
    
    # Compare with Feast
    compare_feast_datahub()
    
    # Export report
    export_datahub_report()
    
    print(f"\n🎯 DataHub Discovery Summary:")
    print(f"   🌐 DataHub UI: {DATAHUB_FRONTEND_URL}")
    print(f"   📊 Features found: {len(features)}")
    print(f"   📝 Report: feature_discovery/datahub_discovery_report.md")
    
    print(f"\n✅ DataHub discovery completed successfully!")

if __name__ == "__main__":
    main() 