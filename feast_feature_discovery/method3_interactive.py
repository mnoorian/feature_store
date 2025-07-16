#!/usr/bin/env python3
"""
Method 3: Interactive Python Discovery

Custom Python script for comprehensive feature exploration with search capabilities.
Best for: Custom exploration and programmatic access.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

def explore_feature_views(store):
    """Explore feature views in detail"""
    print("\n🔍 Feature Views Detail:")
    print("-" * 60)
    
    for fv in store.list_feature_views():
        print(f"\n📊 {fv.name}")
        print(f"   Entities: {fv.entities}")
        print(f"   TTL: {fv.ttl}")
        print(f"   Source: {fv.source.path}")
        print(f"   Features ({len(fv.schema)}):")
        for field in fv.schema:
            print(f"     - {field.name} ({field.dtype}): {field.description}")

def explore_entities(store):
    """Explore entities"""
    print("\n🔑 Entities Detail:")
    print("-" * 60)
    
    for entity in store.list_entities():
        print(f"\n🔑 {entity.name}")
        print(f"   Description: {entity.description}")
        print(f"   Value Type: {entity.value_type}")

def search_features_by_keyword(store, keyword):
    """Search features by keyword"""
    print(f"\n🔍 Searching for '{keyword}':")
    print("-" * 50)
    
    found = False
    
    # Search in feature views
    for fv in store.list_feature_views():
        if keyword.lower() in fv.name.lower() or keyword.lower() in fv.description.lower():
            print(f"📊 Feature View: {fv.name}")
            found = True
        
        # Search in individual features
        for field in fv.schema:
            if keyword.lower() in field.name.lower():
                print(f"   🔸 Feature: {field.name} in {fv.name}")
                found = True
    
    # Search in entities
    for entity in store.list_entities():
        if keyword.lower() in entity.name.lower() or keyword.lower() in entity.description.lower():
            print(f"🔑 Entity: {entity.name}")
            found = True
    
    if not found:
        print(f"❌ No features found matching '{keyword}'")

def get_feature_statistics(store):
    """Get feature store statistics"""
    feature_views = list(store.list_feature_views())
    feature_services = list(store.list_feature_services())
    entities = list(store.list_entities())
    
    total_features = sum(len(fv.schema) for fv in feature_views)
    
    print("\n📈 Feature Store Statistics:")
    print("-" * 60)
    print(f"   Feature Views: {len(feature_views)}")
    print(f"   Feature Services: {len(feature_services)}")
    print(f"   Entities: {len(entities)}")
    print(f"   Total Features: {total_features}")

def main():
    print("🔍 Method 3: Interactive Python Discovery")
    print("=" * 60)
    
    try:
        from feature_store.registry import get_feature_store
        store = get_feature_store()
        
        # Overview statistics
        get_feature_statistics(store)
        
        # Detailed exploration
        explore_entities(store)
        explore_feature_views(store)
        
        # Search examples
        print("\n🔍 Search Examples:")
        print("=" * 60)
        
        search_keywords = ["user", "age", "price", "payment", "session", "transaction"]
        for keyword in search_keywords:
            search_features_by_keyword(store, keyword)
        
        print("\n✅ Interactive discovery completed successfully!")
        
    except ImportError:
        print("❌ Import Error: Make sure you're in the project root directory")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 