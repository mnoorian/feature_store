#!/usr/bin/env python3
"""
Method 4: JSON Metadata Discovery

Explores features using exported JSON metadata.
Best for: External integrations and data cataloging.
"""

import json
import os
from pathlib import Path
from datetime import datetime

def load_metadata(metadata_path="data/feature_metadata.json"):
    """Load feature metadata from JSON file"""
    try:
        with open(metadata_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Metadata file not found: {metadata_path}")
        print("💡 Generate metadata first: python scripts/run_pipeline.py --export-metadata-only")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in metadata file: {e}")
        return None

def explore_metadata_overview(metadata):
    """Show metadata overview"""
    print("📊 Metadata Overview:")
    print("-" * 60)
    print(f"   Export Timestamp: {metadata.get('export_timestamp', 'Unknown')}")
    print(f"   Feature Store: {metadata.get('feature_store', 'Unknown')}")
    print(f"   Entities: {len(metadata.get('entities', []))}")
    print(f"   Feature Views: {len(metadata.get('feature_views', []))}")
    print(f"   Feature Services: {len(metadata.get('feature_services', []))}")

def explore_feature_views_metadata(metadata):
    """Explore feature views from metadata"""
    feature_views = metadata.get('feature_views', [])
    
    print(f"\n📊 Feature Views from Metadata ({len(feature_views)}):")
    print("-" * 60)
    
    for fv in feature_views:
        print(f"\n📊 {fv.get('name', 'Unknown')}")
        print(f"   Entities: {fv.get('entities', [])}")
        print(f"   Features ({len(fv.get('features', []))}): {fv.get('features', [])}")
        print(f"   Source: {fv.get('source_path', 'Unknown')}")
        print(f"   TTL: {fv.get('ttl', 'Unknown')}")

def search_metadata_by_keyword(metadata, keyword):
    """Search metadata by keyword"""
    print(f"\n🔍 Searching metadata for '{keyword}':")
    print("-" * 50)
    
    found = False
    
    # Search in feature views
    for fv in metadata.get('feature_views', []):
        fv_name = fv.get('name', '')
        if keyword.lower() in fv_name.lower():
            print(f"📊 Feature View: {fv_name}")
            found = True
        
        # Search in features
        for feature in fv.get('features', []):
            if keyword.lower() in feature.lower():
                print(f"   🔸 Feature: {feature} in {fv_name}")
                found = True
    
    # Search in entities
    for entity in metadata.get('entities', []):
        entity_name = entity.get('name', '')
        if keyword.lower() in entity_name.lower():
            print(f"🔑 Entity: {entity_name}")
            found = True
    
    if not found:
        print(f"❌ No matches found for '{keyword}'")

def export_summary_report(metadata, output_path="feature_discovery/discovery_report.md"):
    """Export a summary report"""
    print(f"\n📝 Generating summary report: {output_path}")
    
    report_content = f"""# Feature Discovery Report

Generated on: {datetime.now().isoformat()}

## Overview

- **Feature Store**: {metadata.get('feature_store', 'Unknown')}
- **Export Timestamp**: {metadata.get('export_timestamp', 'Unknown')}

## Summary Statistics

- **Entities**: {len(metadata.get('entities', []))}
- **Feature Views**: {len(metadata.get('feature_views', []))}
- **Feature Services**: {len(metadata.get('feature_services', []))}

## Feature Views

"""
    
    # Add feature views
    for fv in metadata.get('feature_views', []):
        report_content += f"### {fv.get('name', 'Unknown')}\n"
        report_content += f"- **Entities**: {', '.join(fv.get('entities', []))}\n"
        report_content += f"- **Features**: {', '.join(fv.get('features', []))}\n"
        report_content += f"- **Source**: {fv.get('source_path', 'Unknown')}\n"
        report_content += f"- **TTL**: {fv.get('ttl', 'Unknown')}\n\n"
    
    # Write report
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(report_content)
    
    print(f"✅ Report saved to: {output_path}")

def main():
    print("🔍 Method 4: JSON Metadata Discovery")
    print("=" * 60)
    
    # Load metadata
    metadata = load_metadata()
    if not metadata:
        return
    
    # Explore metadata
    explore_metadata_overview(metadata)
    explore_feature_views_metadata(metadata)
    
    # Search examples
    print("\n🔍 Search Examples:")
    print("=" * 60)
    
    search_keywords = ["user", "demographic", "transaction", "product"]
    for keyword in search_keywords:
        search_metadata_by_keyword(metadata, keyword)
    
    # Export report
    export_summary_report(metadata)
    
    print("\n✅ Metadata discovery completed successfully!")

if __name__ == "__main__":
    main() 