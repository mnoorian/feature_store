"""
Feature Store Registry Management

This module contains functions for registering features in Feast and exporting metadata
for DataHub integration.
"""

import json
from datetime import datetime
from feast import FeatureStore

from .entities import get_all_entities
from .data_sources import get_all_local_sources, get_all_s3_sources
from .feature_views import get_all_feature_views
from .feature_services import get_all_feature_services


def get_feature_store(repo_path: str = ".") -> FeatureStore:
    """Get initialized feature store"""
    return FeatureStore(repo_path=repo_path)


def register_all_features(repo_path: str = ".", use_s3: bool = False) -> bool:
    """
    Register all features in the feature store
    
    Args:
        repo_path: Path to the feature store repository
        use_s3: Whether to use S3 sources instead of local CSV files
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        store = get_feature_store(repo_path)
        
        # Get all components
        entities = get_all_entities()
        sources = get_all_s3_sources() if use_s3 else get_all_local_sources()
        feature_views = get_all_feature_views()
        feature_services = get_all_feature_services()
        
        # Apply all components
        all_components = entities + sources + feature_views + feature_services
        
        print(f"🔄 Registering {len(all_components)} components in feature store...")
        print(f"- {len(entities)} entities")
        print(f"- {len(sources)} data sources")
        print(f"- {len(feature_views)} feature views")
        print(f"- {len(feature_services)} feature services")
        
        store.apply(all_components)
        
        print("✅ All features successfully registered in the feature store!")
        return True
        
    except Exception as e:
        print(f"❌ Error registering features: {e}")
        return False


def export_metadata(repo_path: str = ".", output_file: str = "data/feature_metadata.json") -> bool:
    """
    Export feature metadata for DataHub integration
    
    Args:
        repo_path: Path to the feature store repository
        output_file: Path to save the metadata JSON file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        store = get_feature_store(repo_path)
        
        # Create metadata structure
        feature_metadata = {
            "export_timestamp": datetime.now().isoformat(),
            "feature_store": "feast_offline_store",
            "data_sources": "Local CSV files in data/transformed/",
            "entities": [],
            "feature_views": [],
            "feature_services": []
        }
        
        # Export entity metadata
        for entity in store.list_entities():
            feature_metadata["entities"].append({
                "name": entity.name,
                "description": entity.description,
                "value_type": str(entity.value_type),
                "join_keys": entity.join_keys
            })
        
        # Export feature view metadata
        for feature_view in store.list_feature_views():
            feature_metadata["feature_views"].append({
                "name": feature_view.name,
                "description": feature_view.description,
                "entities": [entity.name for entity in feature_view.entities],
                "features": [field.name for field in feature_view.schema],
                "ttl": str(feature_view.ttl),
                "source": feature_view.source.name,
                "source_path": feature_view.source.path
            })
        
        # Export feature service metadata
        for feature_service in store.list_feature_services():
            try:
                feature_views = [fv.name for fv in feature_service._features] if hasattr(feature_service, '_features') else []
            except Exception:
                feature_views = []
            
            feature_metadata["feature_services"].append({
                "name": feature_service.name,
                "description": feature_service.description,
                "feature_views": feature_views
            })
        
        # Save metadata to file
        with open(output_file, "w") as f:
            json.dump(feature_metadata, f, indent=2)
        
        print(f"✅ Feature metadata exported to {output_file}")
        print(f"📊 Total: {len(feature_metadata['entities'])} entities, "
              f"{len(feature_metadata['feature_views'])} feature views, "
              f"{len(feature_metadata['feature_services'])} feature services")
        
        return True
        
    except Exception as e:
        print(f"❌ Error exporting metadata: {e}")
        return False


def list_registered_features(repo_path: str = "."):
    """List all registered features in the feature store"""
    try:
        store = get_feature_store(repo_path)
        
        print("📋 Registered Feature Views:")
        for feature_view in store.list_feature_views():
            print(f"- {feature_view.name}: {feature_view.description[:100]}...")
        
        print("\n📋 Registered Feature Services:")
        for feature_service in store.list_feature_services():
            try:
                feature_count = len(feature_service._features) if hasattr(feature_service, '_features') else "unknown"
                print(f"- {feature_service.name}: {feature_count} feature views")
            except Exception as e:
                print(f"- {feature_service.name}: error accessing features - {e}")
        
        print("\n📋 Registered Entities:")
        for entity in store.list_entities():
            print(f"- {entity.name}: {entity.description[:100]}...")
            
    except Exception as e:
        print(f"❌ Error listing features: {e}")


def validate_feature_store(repo_path: str = ".") -> bool:
    """
    Validate the feature store configuration
    
    Args:
        repo_path: Path to the feature store repository
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        store = get_feature_store(repo_path)
        
        # Check if entities exist
        entities = list(store.list_entities())
        if not entities:
            print("⚠️ No entities found in feature store")
            return False
        
        # Check if feature views exist
        feature_views = list(store.list_feature_views())
        if not feature_views:
            print("⚠️ No feature views found in feature store")
            return False
        
        # Check if feature services exist
        feature_services = list(store.list_feature_services())
        if not feature_services:
            print("⚠️ No feature services found in feature store")
            return False
        
        print("✅ Feature store validation passed!")
        print(f"- {len(entities)} entities")
        print(f"- {len(feature_views)} feature views")
        print(f"- {len(feature_services)} feature services")
        
        return True
        
    except Exception as e:
        print(f"❌ Feature store validation failed: {e}")
        return False 