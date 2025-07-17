"""
Feature Store Registry Management

This module contains functions for registering features in Feast and exporting metadata
for DataHub integration.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

import yaml
from feast import FeatureStore
from feast.repo_config import RepoConfig
import datetime as dt


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
        from .entities import get_user_entity, get_product_entity
        from .data_sources import (
            get_user_demographic_source, get_user_behavior_source,
            get_transaction_source, get_product_source
        )
        from .feature_views import (
            get_user_demographic_features, get_user_behavior_features,
            get_transaction_features, get_product_features
        )
        from .feature_services import (
            get_user_feature_service, get_product_feature_service,
            get_behavior_feature_service
        )
        
        # Get feature store
        store = get_feature_store(repo_path)
        
        # Apply feature store
        store.apply([
            get_user_entity(),
            get_product_entity(),
            get_user_demographic_source(),
            get_user_behavior_source(),
            get_transaction_source(),
            get_product_source(),
            get_user_demographic_features(),
            get_user_behavior_features(),
            get_transaction_features(),
            get_product_features(),
            get_user_feature_service(),
            get_product_feature_service(),
            get_behavior_feature_service()
        ])
        
        print("✅ All features registered successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error registering features: {e}")
        return False


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
        
        # Check entities
        entities = store.list_entities()
        print(f"📊 Found {len(entities)} entities")
        
        # Check feature views
        feature_views = store.list_feature_views()
        print(f"📊 Found {len(feature_views)} feature views")
        
        # Check feature services
        feature_services = store.list_feature_services()
        print(f"📊 Found {len(feature_services)} feature services")
        
        return True
        
    except Exception as e:
        print(f"❌ Feature store validation failed: {e}")
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
        
        # Load config using PyYAML
        with open(os.path.join(repo_path, "configs", "feature_store.yaml"), "r") as f:
            config = yaml.safe_load(f)
        
        # Create Feast standard metadata structure
        feature_metadata = {
            # Feast standard metadata
            "project": config.get("project"),
            "provider": config.get("provider"),
            "online_store": config.get("online_store", {}),
            "offline_store": config.get("offline_store", {}),
            "registry": config.get("registry", {}),
            
            # Export metadata
            "export_timestamp": datetime.now().isoformat(),
            "export_version": "100",
            "export_format": "feast_standard",
            
            # Feast core components
            "entities": [],
            "data_sources": [],
            "feature_views": [],
            "feature_services": []
        }
        
        # Export entity metadata (Feast standard)
        for entity in store.list_entities():
            created_ts = getattr(entity, 'created_timestamp', None)
            if isinstance(created_ts, dt.datetime):
                created_ts = created_ts.isoformat()
            updated_ts = getattr(entity, 'last_updated_timestamp', None)
            if isinstance(updated_ts, dt.datetime):
                updated_ts = updated_ts.isoformat()
            entity_metadata = {
                "name": entity.name,
                "description": entity.description or "",
                "value_type": str(entity.value_type),
                "join_key": getattr(entity, 'join_key', getattr(entity, 'join_keys', None)),
                "tags": getattr(entity, 'tags', []),
                "owner": getattr(entity, 'owner', None),
                "created_timestamp": created_ts,
                "last_updated_timestamp": updated_ts
            }
            feature_metadata["entities"].append(entity_metadata)
        
        # Export data source metadata (Feast standard)
        data_sources = set()
        for feature_view in store.list_feature_views():
            source = feature_view.source
            if source.name not in data_sources:
                data_sources.add(source.name)
                source_metadata = {
                    "name": source.name,
                    "type": source.__class__.__name__,
                    "path": getattr(source, 'path', None),
                    "timestamp_field": getattr(source, 'timestamp_field', None),
                    "description": getattr(source, 'description', None),
                    "tags": getattr(source, 'tags', []),
                    "owner": getattr(source, 'owner', None)
                }
                feature_metadata["data_sources"].append(source_metadata)
        
        # Export feature view metadata (Feast standard)
        for feature_view in store.list_feature_views():
            # Get feature schema details
            schema_fields = []
            for field in feature_view.schema:
                schema_fields.append({
                    "name": field.name,
                    "dtype": str(field.dtype),
                    "description": field.description or "",
                    "tags": getattr(field, 'tags', [])
                })
            
            created_ts = getattr(feature_view, 'created_timestamp', None)
            if isinstance(created_ts, dt.datetime):
                created_ts = created_ts.isoformat()
            updated_ts = getattr(feature_view, 'last_updated_timestamp', None)
            if isinstance(updated_ts, dt.datetime):
                updated_ts = updated_ts.isoformat()
            feature_view_metadata = {
                "name": feature_view.name,
                "description": feature_view.description or "",
                "entities": [entity if isinstance(entity, str) else entity.name for entity in feature_view.entities],
                "schema": schema_fields,
                "ttl": str(feature_view.ttl) if feature_view.ttl else None,
                "source": {
                    "name": feature_view.source.name,
                    "type": feature_view.source.__class__.__name__
                },
                "tags": getattr(feature_view, 'tags', []),
                "owner": getattr(feature_view, 'owner', None),
                "created_timestamp": created_ts,
                "last_updated_timestamp": updated_ts,
                
                # DataHub specific fields
                "datahub": {
                    "urn": f"urn:li:dataset:(urn:li:dataPlatform:feast,{feature_view.name},PROD)",
                    "platform": "feast",
                    "properties": {
                        "feature_count": len(feature_view.schema),
                        "entity_count": len(feature_view.entities),
                        "ttl_days": feature_view.ttl.days if feature_view.ttl else None,
                        "update_frequency": "daily", # Could be extracted from description
                        "business_use_cases": extract_business_use_cases(feature_view.description or ""),
                        "code_logic_url": extract_code_logic_url(feature_view.description or "")
                    }
                }
            }
            feature_metadata["feature_views"].append(feature_view_metadata)
        
        # Export feature service metadata (Feast standard)
        for feature_service in store.list_feature_services():
            try:
                feature_views = [fv.name for fv in feature_service._features] if hasattr(feature_service, '_features') else []
            except Exception:
                feature_views = []
            
            created_ts = getattr(feature_service, 'created_timestamp', None)
            if isinstance(created_ts, dt.datetime):
                created_ts = created_ts.isoformat()
            updated_ts = getattr(feature_service, 'last_updated_timestamp', None)
            if isinstance(updated_ts, dt.datetime):
                updated_ts = updated_ts.isoformat()
            feature_service_metadata = {
                "name": feature_service.name,
                "description": feature_service.description or "",
                "feature_views": feature_views,
                "tags": getattr(feature_service, 'tags', []),
                "owner": getattr(feature_service, 'owner', None),
                "created_timestamp": created_ts,
                "last_updated_timestamp": updated_ts,
                
                # DataHub specific fields
                "datahub": {
                    "urn": f"urn:li:dataset:(urn:li:dataPlatform:feast,{feature_service.name},PROD)",
                    "platform": "feast",
                    "properties": {
                        "feature_view_count": len(feature_views),
                        "total_features": sum(len(store.get_feature_view(fv_name).schema) for fv_name in feature_views if store.get_feature_view(fv_name)),
                        "service_type": "FeatureService"
                    }
                }
            }
            feature_metadata["feature_services"].append(feature_service_metadata)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Save metadata to file
        with open(output_file, "w") as f:
            json.dump(feature_metadata, f, indent=2)
        
        print(f"✅ Feature metadata exported to {output_file}")
        print(f"📊 Total: {len(feature_metadata['entities'])} entities, "
              f"{len(feature_metadata['data_sources'])} data sources, "
              f"{len(feature_metadata['feature_views'])} feature views, "
              f"{len(feature_metadata['feature_services'])} feature services")
        
        return True
        
    except Exception as e:
        print(f"❌ Error exporting metadata: {e}")
        return False


def extract_business_use_cases(description: str) -> List[str]:
    """Extract business use cases from feature view description"""
    use_cases = []
    if "**Business Use Cases:**" in description:
        try:
            use_cases_section = description.split("**Business Use Cases:**")[1].split("**")[0]
            use_cases = [uc.strip() for uc in use_cases_section.split(",") if uc.strip()]
        except:
            pass
    return use_cases


def extract_code_logic_url(description: str) -> Optional[str]:
    """Extract code logic URL from feature view description"""
    if "**Code Logic:**" in description:
        try:
            url_section = description.split("**Code Logic:**")[1].split("**")[0]
            return url_section.strip()
        except:
            pass
    return None


def list_registered_features(repo_path: str = ".") -> Dict[str, Any]:
    """List all registered features in the feature store"""
    try:
        store = get_feature_store(repo_path)
        
        features = {
            "entities": [],
            "feature_views": [],
            "feature_services": []
        }
        
        # List entities
        for entity in store.list_entities():
            features["entities"].append({
                "name": entity.name,
                "description": entity.description,
                "value_type": str(entity.value_type)
            })
        
        # List feature views
        for feature_view in store.list_feature_views():
            features["feature_views"].append({
                "name": feature_view.name,
                "description": feature_view.description,
                "entities": [entity.name for entity in feature_view.entities],
                "features": [field.name for field in feature_view.schema]
            })
        
        # List feature services
        for feature_service in store.list_feature_services():
            try:
                feature_views = [fv.name for fv in feature_service._features] if hasattr(feature_service, '_features') else []
            except Exception:
                feature_views = []
            
            features["feature_services"].append({
                "name": feature_service.name,
                "description": feature_service.description,
                "feature_views": feature_views
            })
        
        return features
        
    except Exception as e:
        print(f"❌ Error listing features: {e}")
        return {} 